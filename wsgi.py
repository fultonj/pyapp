import configparser
import rados
import socket

from flask import Flask
application = Flask(__name__)

@application.route('/')
def show_ceph_test_results():
    results = ceph_test()
    return results+"\r\n", 200, { 'Content-Type': 'text/plain' }

def ceph_test():
    ceph_conf = 'ceph.conf'
    try:
        with open(ceph_conf, 'r') as f:
            msg = "Using ceph.conf with the following:"
            msg += "\r\n"
            msg += f.read()
            msg += "\r\n"
        try:
            # check if ceph mon service is exposed
            config = configparser.ConfigParser()
            config.read(ceph_conf)
            ip, port = mon_host = config['global']['mon_host'].split(':')
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            location = (str(ip), int(port))
            result_of_check = a_socket.connect_ex(location)
            msg += "\r\n"
            if result_of_check == 0:
                msg += "%s:%s is open" % (ip, port)
            else:
                msg += "%s:%s is closed" % (ip, port)
            msg += "\r\n"
            a_socket.close()

            with open('ceph.client.openstack.keyring', 'r') as f:
                msg += "Using ceph.client.openstack.keyring with the following:"
                msg += "\r\n"
                msg += f.read()
                msg += "\r\n"
            try:
                cluster = rados.Rados(conffile='ceph.conf')
                cluster.connect()
                msg += "Connected to ceph"
                msg += "\r\n"
                mon_ip = cluster.conf_get('mon_host')
                msg += "mon_host: " + str(mon_ip)
                msg += "\r\n"
                fsid = cluster.conf_get('fsid')
                msg += "fsid: " + str(fsid)
                msg += "\r\n"
                pools = cluster.list_pools()
                msg += "pools: " + str(",".join(pools))
                msg += "\r\n"
                try:
                    ioctx = cluster.open_ioctx('volumes')
                    msg += "Connected to volumes pool with open_ioctx"
                    msg += "\r\n"
                    ioctx.aio_write_full('foo', 'bar')
                    msg += "Write 'bar' to new object called 'foo'"
                    msg += "\r\n"
                    ioctx.aio_write_full('baz', 'qux')
                    msg += "Write 'baz' to new object called 'qux'"
                    msg += "\r\n"
                    i = 0
                    for o in ioctx.list_objects():
                        i += 1
                    msg += "Counted %s objects" % i
                    msg += "\r\n"
                    foo = ioctx.read('foo', 3, 0)
                    msg += "read 3 characters of foo: " + str(foo)
                    msg += "\r\n"
                    baz = ioctx.read('baz', 3, 0)
                    msg += "read 3 characters of baz: " + str(baz)
                    msg += "\r\n"
                    msg += "Removing foo and baz objects"
                    ioctx.aio_remove('foo')
                    ioctx.aio_remove('baz')
                    ioctx.close()
                    cluster.shutdown()
                except:
                    msg += "Could not open_ioctx"
            except:
                msg += "Could not connect to ceph"
        except:
          msg += "Did you UPDATE the app to include YOUR cephx key?"
    except:
      msg += "Did you UPDATE the app to include YOUR ceph.conf (and cephx key)?"
    return msg


if __name__ == '__main__':
    application.run(debug = True)
