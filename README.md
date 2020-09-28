# pyapp

Simple Python App to test Ceph connections.

If cephx key called `ceph.client.openstack.keyring` and a `ceph.conf`
are placed in the same directory as the `wsgi.py` app, then the app
uses them to  connect to the Ceph cluster. If it can connect it will
then write and remove test data on that cluster's `volumes` pool and
show the results of doing this over HTTP.

## Create
```
oc login -u developer -p developer https://api.crc.testing:6443
oc new-project pyapp
oc new-app python~https://github.com/fultonj/pyapp.git
oc expose svc/pyapp
```

## Read
```
oc get route pyapp
URL=$(oc get route pyapp --template '{{ .spec.host }}')
curl $URL
```

## Update
```
oc start-build pyapp -F --from-dir=.
```

## Delete
```
oc delete project pyapp
```
