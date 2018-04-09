Fibonacci number rest service
===========================
## Introduction
This is a rest service that returns Fibonacci number sequence with following features:
* Time complexity is O(logn)
* Support pagination
* By default, be able to support up to Fibonacci(1048576), where the parameter is 2 of power 20.
* With cache configured, be able to support larger Fibonacci(n) request

## REST API
* **URL**

    /api/fibonaci/<b>n</b>

    where `n=[int]`: Fibonacci Function parameter

* **Method:**  `GET`
  
*  **URL Params**

   **Optional:**
   
   `offset=[int]`: For pagination purpose. Indicates the offset of the first Fibonacci number returned to client. Default value is 0.

   `limit=[int]`: For pagination purpose. Indicates the max number of Fibonacci number that can return to client. Default value is 100.

* **Success Response:**
  
    * **Code:** 200 <br />
    **Content:** Example of  ```curl 'http://127.0.0.1:5000/api/fibonacci/10?offset=2&limit=3'```
```json
{
  "results": {
    "data": [
      1,
      2,
      3
    ],
    "links": {
      "next": "/api/fibonacci/10?offset=5&limit=3"
    },
    "pagination": {
      "limit": 3,
      "offset": 2,
      "total": 11
    }
  }
}
```
 
* **Error Response:**

  * **Code:** 403  <br />
    **Content:** ```{"message": "The Fibonacci parameter is too larger. For now, the limit is 1024"}```

    **Content:** `{"message": "'offset' should be an integer and be in the range of [0, n]." }`

    **Content:** `{ "message": "'limit' should be an integer and be in the range of (0, 1000]."}`    

    **Content:** `{"message": "page is not found" }` 

    ... 

* **Sample Call:**

  Return all number sequence of Fibonacci(5):
  
  ```curl 'http://127.0.0.1:5000/api/fibonacci/5```
  
  Return the last 10 numbers of Fibonacci(100) number sequence:
  
  ```curl 'http://127.0.0.1:5000/api/fibonacci/100?offset=90```
  
  Return the first 5 numbers of Fibonacci(100) number sequence:
  
  ```curl 'http://127.0.0.1:5000/api/fibonacci/100?limit=5```
  
  Return the last number of Fibonacci(1000) number sequence:
  
  ```curl 'http://127.0.0.1:5000/api/fibonacci/1000?offset=1000&limit=1```


## Deployment
### set up single node environment automatically through vagrant
```
1. Install vagrant and virtualbox
2. Open PowerShell (for windows) and change directory to source code directory
3. vagrant up (It may take a while for box downloading and provisioning)
4. vagrant ssh (Login in the box)
5. curl 'http://localhost:8000/api/fibonacci/5'
```
### set up development environment manually
Setup for development environment
```
sudo yum -y update
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo yum -y install python36u-pip
sudo yum -y install python36u-devel
sudo pip3.6 install virtualenv
python3.6 /usr/lib/python3.6/site-packages/virtualenv.py fibonacci
source fibonacci/bin/activate
pip install flask
pip install gunicorn
git clone https://url-to-repository
export PYTHONPATH=$PYTHONPATH:/code-directory/
python /code-directory/application/main.py

Open another console and input
curl 'http://localhost:5000/api/fibonacci/5'

```

## Some thought about future work
 
It could become a complex problem if this service should support real big parameter 'n' in Fibonacci(n), like number larger than one billion. One of possible architecture to address this complex problem is shown in following diagram 1.

![Alt text](doc/fibonaci_service_architecture.png?raw=true "Fibonacci Rest Service Architecture") 

<p align="center">
Diagram 1. Overall architecture
</p>

### Strategy to calculate and cache Fibonacci number

Here, the responsibility of Fibonacci calculation and Fibonacci request servicing are taken by Spark cluster and WSGI cluster respectively for following reasons:

* Relieve WSGI servicers of computation burden to improve serving latency
* Leverage modern computation framework to compute Fibonacci number in parallel

According to following formulas proposed by the Prof. Edsgar W Dijkstra around 1978:

F(2n-1) = F(n-1)*F(n-1) + F(n)*F(n)

F(2n) = ( 2*F(n-1) + F(n) )*F(n)

As illustrated in Diagram 2, Fibonacci numbers calculation can be parallelized in following condition:
Roughly speaking, if (i-1) layer’s Fibonacci numbers have been calculated, the computation of (i) layer’s Fibonacci numbers can be parallelized. With the increase of layer number, this kind of parallelism becomes more effective because the number of Fibonacci number doubles every layer. Theoretically, the time of each layer’s Fibonacci number computation could be constant if there is enough computation resources. We ignore the computation details as each layer’s Fibonacci number computation can be treated as typical Map Reduce program. By the way, for the sake of efficiency, the computation result should be loaded/inserted into the distributed key-value store in batch instead of one by one.

As for the distributed key-value store, popular key-value nosql, like HBase, could be a good candidate as they already take good care of system’s scalability, availability, performance and etc…
 

![Alt text](doc/fibonacci_layer.png?raw=true "Logic layer of Fibonacci sequence ")

<p align="center">
Diagram 2. Fibonacci sequence number organized 
</p>

### Strategy to serve Fibonacci request

After receiving requests from different clients, Nginx servers work as load balancer to pass the request to WSGI servers. For each WSGI server, it executes following pseudo code:

* Fibonacci(n) is the number that client requests and 
* Fibonacci(m) is the largest number cached in Key-Value store, which means that all Fibonacci(k) [k<m] have also been cached. System Management Service will notify each WSGI servers to update this value once a batch of Fibonacci number has been loaded into the distributed key-value store.

```
if (m >= n): 
  Retrieve Fibonacci(n) from cache directly and return
else:
  Layers = math.ceil(math.log2(n)) - math.ceil(math.log2(m)) // estimate the cost of computation based on cache
  If Layers <= MAX_FIBONACI_LAYER: # MAX_FIBONACI_LAYER is a configurable parameter
    Calculate Fibonacci(n) recursivly according to following formulas:
      F(2n-1) = F(n-1)*F(n-1) + F(n)*F(n)
      F(2n) = (2*F(n-1) + F(n))*F(n)
  Else:  
    Just return and info client that the Fibonacci number is too large for the system to calculate for now
```
In this way, WSGI servers rely on distributed cache heavily to satisfy client request very fast and just invoke light weight computation if necessary. And they also possesses some kind of intelligence to protect itself from being ruined by denying really big Fibonacci number request that is out of its current capability.

### Strategy to trigger Fibonacci number computation

Are the clients happy with this Fibonacci number service?

Does the distributed key-value store cache enough Fibonacci number to serve our clients? 

Should larger Fibonacci number be calculated and cached in advance?

To answer these questions, we have to collect data from WSGI servers. One typical way is to ask each WSGI server to write a log in its local file system for each request it serves, no matter it is successful or not. And some kind of log collection/analysis system, like ELK, could be leveraged to aggregate and analyze the log. In this way, our system management servers can easily retrieve different kind of service metrics, like 99th percentile latency. Then, it can easily make a decision if it should trigger Fibonacci number computation according to SLA committed to our clients.
