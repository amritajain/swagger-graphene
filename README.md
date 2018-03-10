# Swagger to Graphene

This library can be used to convert Swagger schema into dynamic Graphene models. The system can be deloyed on AWS stack using Serverless framework and be used to get your APIs up instantly.

  - Converts swagger models into GraphQL based APIs.
  - Dynamic Graphene models
  - Serverless framework for deployment


### Installation

Prerequisites:
- python 3.6
- pip3
- npm

Setup virtual env

```sh
$ virtualenv -p $(which python3.6) runLocal
$ source runLocal/bin/activate
```
Project requirements installations:
```sh
$ pip3 install -r src/requirements.txt
```
Install serverless
```sh
$ npm install -g serverless
$ npm install --save-dev serverless-python-requirements
```

Setting up source data
Open data/databse.csv and edit it to provide the information about your APIs in csv format.
* Root entity: This would be the root note of Graphql query.
* Swagger souce url: Provide the endpoint for Swagger schema definition.
* API endpoint: Provide the endpoint for API. (only GETs are supports for now)

| Root Entity | Swagger Source Url | API Endpoint|
| ------ | ------ | ----|
| Pet | file:///data/swagger_definition.json | https://25e3b8c4-e01f-423b-a0e0-07b261023e71.mock.pstmn.io/complicatedPet|

Deployment
Deploy using serverless framework. You would need AWS's account id.
```sh
$ serverless deploy --accountID <AWS::AccountId> --stage <dev|qa|prod>
```

### Running Unittests
Tests are under tests/unittests folder and can be run using pytest or directly via PyCharm.
```sh
$ pytest tests/
```

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
