# pyapp

Simple Python App for use with Code Ready Containers

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
