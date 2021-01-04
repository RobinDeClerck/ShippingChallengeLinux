# Linux Shipping Challenge

## Assignment
* Create your own kubernetes stack with 1 worker
* Containerized application on worker
  * When surname changes in DB, webpage changes automatically
    ![Workflow](https://cdn.discordapp.com/attachments/668890794882629662/793964865604812820/Untitled_picture.png)
  * When layout of webpage changes, the worker will display the new layout automatically
  * Use the webstack which is assigned to you

### My assigned webstack
| Webserver | Database | Script Language |
| ------------- |:-------------:| -----:|
| Lighttpd | MySQL | Python |

### Points
**10/20 - stack in Docker** \
**14/20 - mk8s cluster with 1 worker**


* Vagrant
* Extra worker
* Management webplatform for containers:

|Webserver|
|:---------:|
|K8s Dashboard|

* Something else than MK8s with the same purpose
* (A practical linux joke for docents / a linux koan to enlighten your docents = extra point)

## Installation
### Create the Python project
I used the Python package [web.py](https://webpy.org/) to create my Python application.
I tried to use Flask but Lighttpd's support for Python is old and caused a lot of problems when trying to host the application.

In the Python application I created a return with "Hi {firstname}' with 'firstname' coming from the database.

**Database connection function:**
```Python
def setup_database_connection():
    # CONNECTION TO SQL SERVER #
    import mysql.connector

    mydb = mysql.connector.connect(
        user=DATABASE_USER,
        passwd=DATABASE_PASSWORD,

        host=DATABASE_HOST,
        port=DATABASE_PORT,

        database=DATABASE_DB,
    )
    return mydb
```

**To get the data out of the database:**
```Python
# DB Connection
database = setup_database_connection()
cursor = database.cursor()

db_query = 'SELECT surname FROM User WHERE userId = 1'
cursor.execute(db_query)

surname = cursor.fetchone()[0]
```

### Dockerfile
The dockerfile is needed to build and run the application inside a container.

In the dockerfile I write all needed dependencies that need to be installed.

```Dockerfile
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install lighttpd
RUN apt-get install -y python3-pip python3-dev

ENV LIGHTTPD_VERSION=1.4.55-r1

RUN apt-get install lighttpd -y

COPY ./etc/lighttpd/* /etc/lighttpd/


EXPOSE 80

WORKDIR /var/www/shippingchallenge

COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./ .

CMD ["lighttpd","-D","-f","/etc/lighttpd/lighttpd.conf"]
```
**Main steps:**
- Start Ubuntu and update
- Install Lighttpd
- Expose port 80 (this is the port inside the docker container that will be exposed)
- Install my application
- Install the dependencies in requirements.txt
- State the start command


### Docker Hub
I put the project online so I (and Kubernetes) can download the project on any machine via:
`robindeclerck/shippingchallenge`

When I push a new version to GitHub, Docker Hub wil automatically create a new version via automated builds.

### Kubernetes
**Deployment**\
This will download the image from Docker Hub `robindeclerck/shippingchallenge` and create 3 pods.

```Yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shippingchallenge-deployment
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lighttpd
  template:
    metadata:
      labels:
        app: lighttpd
    spec:
      containers:
        - name: lighttpd
          image: robindeclerck/shippingchallenge
          ports:
            - containerPort: 80
              name: http
```
**Service**\
The service needs to attach the deployment via selector, app.

```Yaml
apiVersion: v1
kind: Service
metadata:
  name: shippingchallenge-service
  namespace: default
spec:
  type: ClusterIP
  ports:
    - port: 80
  selector:
    app: lighttpd
```
**Ingress**\
The Ingress needs to specify the service that needs to be used for the port via 'serviceName' 
```Yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: shippingchallenge-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
    - host: shippingchallenge.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              serviceName: shippingchallenge-service
              servicePort: 80
```
You also need to specify 'shippingchallenge.local' in your hosts file: \
`sudo nano /etc/hosts` and add the ip of the ingress and the host (shippingchallenge.local).

If you just go to the IP of the application you will get a "NGINX ERROR NOT FOUND".

## Ubuntu
I installed the latest [Ubuntu 20.10](https://ubuntu.com/download/desktop) on my VirtualBox.\
*Note: Using default 10GB space is not enough for this project*

**Install Curl:**
```sudo apt-get install curl```

**Install Docker:**\
https://docs.docker.com/engine/install/ubuntu/

I had a problem where docker did not have permissions to execute containers I found the fix on stackoverflow (using docker with sudo != ok): \
https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue

**Install Kubernetes:**\
https://kubernetes.io/docs/tasks/tools/install-kubectl/

**Install Minikube (needed for ingress-controller):**\
https://v1-18.docs.kubernetes.io/docs/tasks/tools/install-minikube/

**Start Minikube to install itself:** \
`minikube start`

For the Ingress we need an Ingress controller, otherwise there will no IP be added to the Ingress: \
```minikube addons enable ingress```

So the Ingress will get an 'ADDRESS'\
![Example](https://cdn.discordapp.com/attachments/668890794882629662/793975308705071104/Capture.PNG)

---
After the installation I started the application (the Deployment, Service, Ingress are all in the same file seperated with ---): \
`kubectl apply -f deploy.yaml`

The project will install and run after this command. This command is also used when changing the deploy.yaml file


## Kubernetes dashboard
Install Kubernetes dashboard:
https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

You will need a user and token for the dashboard:
https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md

You can access Dashboard using the kubectl command-line tool by running the following command:\
`kubectl proxy`

To go to the dashboard:\
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/discovery?namespace=default

### Debugging
It's possible to debug a kubernetes deployment:\
`kubectl get pods`\
![Example](https://cdn.discordapp.com/attachments/668890794882629662/794585998033289236/unknown.png)

`kubectl exec -it shippingchallenge-deployment-79998c989c-6jvvq sh`

I used this to check if my service/deployment worked by installing curl and using `curl shippingchallenge-service` to check if my application was running correctly inside Kubernetes

This is also really handy to check your database deployment:\
![Example](https://cdn.discordapp.com/attachments/668890794882629662/794588040873246770/unknown.png)

#### Change database row
Login: \
`$ mysql -u user -p'password'` \
Show databases: \
`mysql> SHOW DATABASES;` \
Insert new row: \
`mysql> USE ShippingChallenge;` \
`mysql> SELECT * FROM User;` \
`mysql> UPDATE User SET surname = "Bob" WHERE userId = 1;`


##### To restart a deployment (will also update the image):
`kubectl get deployment`\
`kubectl rollout restart deployment [deployment_name]`