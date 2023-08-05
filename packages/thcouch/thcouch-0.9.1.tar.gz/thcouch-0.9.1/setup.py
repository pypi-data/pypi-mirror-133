# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thcouch',
 'thcouch.core',
 'thcouch.core.attachment',
 'thcouch.core.db',
 'thcouch.core.db.design_docs',
 'thcouch.core.doc',
 'thcouch.core.index',
 'thcouch.core.server',
 'thcouch.orm',
 'thcouch.orm.decl']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'json5>=0.9.6,<0.10.0',
 'pyyaml>=6.0,<7.0',
 'thresult>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'thcouch',
    'version': '0.9.1',
    'description': 'TangledHub thcouch library',
    'long_description': '[![Build][build-image]]()\n[![Status][status-image]][pypi-project-url]\n[![Stable Version][stable-ver-image]][pypi-project-url]\n[![Coverage][coverage-image]]()\n[![Python][python-ver-image]][pypi-project-url]\n[![License][bsd3-image]][bsd3-url]\n\n\n# thcouch\n\n## Overview\nTangledHub library for couchdb with a focus on asynchronous functions\n\n## Licensing\nthcouch is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details\n\n## Installation\n```bash\npip instal thcouch\n```\n\n---\n\n## Testing\n```bash\ndocker-compose build thcouch-test ; docker-compose run --rm thcouch-test\n```\n\n## Building\n```bash\ndocker-compose build thcouch-build ; docker-compose run --rm thcouch-build\n```\n\n## Publish\n```bash\ndocker-compose build thcouch-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thcouch-publish\n```\n\n---\n\n## Usage\n\n## Database\nCouchDB provides a RESTful HTTP API for \nreading and updating (add, edit, delete) database documents\n\n### create\n```python\n\'\'\'\ndescription:\n    creates the database \n    by providing uri and database name\n\nparameters: \n    uri: str\n    db: str\n\nreturns:\n    PutDbOk\n\'\'\'\n\n# creates database by given uri and db(name)\ndb: CouchDatabase = (await put_db(uri=COUCH_URI, db=DATABASE_NAME)).unwrap()\n```\n\n### Delete\n```python\n\'\'\'\ndescription:\n    deletes the database\n     by providing uri and database name\n\nparameters: \n    uri: str\n    db: str\n\nreturns:\n    DeleteDbOk\n\'\'\'\n\n# deletes database by given uri and db(name)\n(await delete_db(uri=COUCH_URI, db=DATABASE_NAME)).unwrap()\n```\n\n## Loader\n\n### setup\nloader reads file configurations\nsuports toml, yaml, json and json5 files\n```python\n\'\'\'\ndescription:\n    create instance of CouchLoader\n    by providing CouchDatabase object and path to file\n\nparameters: \n    db: CouchDatabase\n    path: str\n\nreturns:\n    CouchLoader \n\'\'\'\n\n# instantiate CouchLoader by given db and path\nloader: CouchLoader = CouchLoader(db=DB, path=PATH_TO_FILE)\n```\n\n### example of config files for loader:\n### toml file\n```\n[User]\n_type = "model"\n_id = "string, required=True, default=uuid4"\n_rev = "string, should_get=lambda value: False if value is None else True"\nemail = "string, validator=\'email\'"\nphone = "Field(string)"\nage = "int"\n```\n\n### yaml file\n```\nUser:\n  _type: "model"\n  _id: "string, required=True, default=uuid4"\n  _rev: "string, should_get=lambda value: False if value is None else True"\n  usertype: "string, default=\'company\', values=[\'company\', \'individual\']"\n  email: "string, validator=\'email\'"\n  phone: "Field(string)"\n  age: "int"\n```\n\n### json file\n```\n{\n    "User": {\n        "_type": "model",\n        "_id": "string, required=True, default=uuid4",\n        "_rev": "string, should_get=lambda value: False if value is None else True",\n        "usertype": "string, default=\'company\', values=[\'company\', \'individual\']",\n        "email": "string, validator=\'email\'",\n        "phone": "Field(string)",\n        "age": "int"\n    }\n}\n```\n\n### json5 file\n```\n{\n    // user model\n    "User": {\n        "_type": "model",\n        "_id": "string, required=True, default=uuid4",\n        "_rev": "string, should_get=lambda value: False if value is None else True",\n        "usertype": "string, default=\'company\', values=[\'company\', \'individual\']",\n        "email": "string, validator=\'email\'",\n        "phone": "Field(string)",\n        "age": "int"\n    }\n}\n```\n\n\n## Model\nDocuments(Model) are the primary unit of data \nin CouchDB and consist of any number of fields and attachments\n\nSingle document updates (add, edit, delete) are all or nothing,\neither succeeding entirely or failing completely.\nThe database never contains partially saved or edited documents\n\n# TODO: explain model types\n### setup\n```python\n\'\'\'\ndescription:\n    load BaseModel type using CouchLoader\n    creates instance of BaseModel\n\nreturns:\n    BaseModel\n\'\'\'\n\n# load Model type from file\nUser: type = loader.User\n\n# create User/BaseModel object\nuser0: User = User()\n```\n\n### create/add\nThe Add method creates a new named document\n```python\n\'\'\'\ndescription:\n    add function created document into database\n    call on model or model instance\n    \n    if call on model:\n        parameters: \n            self: BaseModel\n\nreturns:\n    BaseModel\n\'\'\'\n\n# save model instance to database - call on model\nuser1_0: User = (await User.add(user0)).unwrap()\n\n# save model instance to database - call on model instance\nuser1_0: User = (await user0.add()).unwrap()\n```\n\n### get\nReturns document by the specified docid from the specified db.\nUnless you request a specific revision, the latest revision of the document will always be returned\n```python\n\'\'\'\ndescription:\n    get function gets existing documents\n    from database by providing document id and document rev \n\nparameters: \n    docid: str,\n    rev: None | str = None\n\nreturns:\n    BaseModel\n\'\'\'\n\n# get model from database by given id and rev, if rev is not passed document will be latest\nuser0_1: User = (await User.get(docid = user1_0._id, rev = user1_0._rev)).unwrap()\n```\n\n### all\nExecutes the built-in _all_docs view,\nreturning all of the documents in the database\n```python\n\'\'\'\ndescription:\n    all function gets list of existing documents \n    from database \n\nreturns:\n    list[BaseModel]\n\'\'\'\n\n# gets list of all models from database\nusers0: list[User] = (await User.all()).unwrap()\n```\n\n### find\nFind documents using a declarative JSON querying syntax. Queries can use the built-in _all_docs index or custom indexes, specified using the _index endpoint.\n```python\n\'\'\'\ndescription:\n    find function gets list of existing documents \n    from database \n    by providing selector/dict as query  \n\nparameters: \n    selector: dict,\n    limit: None | int = None,\n    skip: None | int = None,\n    sort: None | list[dict | str] = None,\n    fields: None | list[str] = None,\n    use_index: None | (str | list[str]) = None,\n    r: None | int = None,\n    bookmark: None | str = None,\n    update: None | bool = None,\n    stable: None | bool = None\n\nreturns:\n    tuple[list[BaseModel], bookmark: str, warning: str]\n\'\'\'\n\nselector = {\n            \'usertype\': \'company\'\n        }\n\n# gets tuple of all models, bookmark, warning from database by given selector\nuser0_1: tuple[list[User], str, str] = (await User.find(selector = selector)).unwrap()\n```\n\n### delete\nMarks the specified document as deleted by adding a field\n_deleted with the value true.\nDocuments with this field will not be returned\nwithin requests anymore, but stay in the database.\nYou must supply the current (latest) revision\nby using the rev parameter.\n```python\n\'\'\'\ndescription \n    delete function deletes user from database\n    call on model or model instance\n    \n    if call on model:\n        parameters:\n            self: BaseModel\n            batch: None | str = None\n\nreturns:\n    BaseModel\n\'\'\'\n\n# delete model instance from database - call on model\nuser0_1: User = (await User.delete(user_0)).unwrap()\n\n# delete model instance from database - call on model instance\nuser0_1: User = (await user_0.delete()).unwrap()\n```\n\n### update\nWhen updating an existing document, the current document revision\nmust be included in the document (i.e. the request body),\nas the rev query parameter\n```python\n\'\'\'\ndescription:\n    update function updates existing document \n    from database \n    by providing fields to update\n\nparameters:\n    doc: dict, \n    batch: None | str = None, \n    new_edits: None | bool = None\n\nreturns:\n    BaseModel\n\'\'\'\n\ndoc_update: dict = {\n    \'email\': \'user@user.com\'\n}\n\n# update model instance from database with given dict\n# with fields as keys\nuser0_1: User = (await user_0.update(doc = doc_update)).unwrap()\n```\n\n### bulk get\nThis method can be called to query several documents in bulk. It is well suited for fetching a specific revision of documents, as replicators do for example, or for getting revision history\n\n```python\n\'\'\'\ndescription:\n    bulk get function gets a list of documents \n    from database by\n    providing the ids and revs of specific documents\n    \nparameters:\n    docs: list[dict],\n    revs: None | bool = None\n\nreturns:\n    list[BaseModel]\n\'\'\'\n\ndoc1: dict = {\'id\': user1._id, \'rev\': user1.rev}\n\n# gets all models by given list of dicts\nuser0_1: list[User] = (await User.bulk_get(list[doc1])).unwrap()\n```\n\n### bulk docs\nThe bulk document API allows you to create and update multiple documents at the same time within a single request. The basic operation is similar to creating or updating a single document, except that you batch the document structure and information.\nWhen creating new documents the document ID (_id) is optional.\n\nFor updating existing documents, you must provide the document ID, revision information (_rev), and new document values.\nIn case of batch deleting documents all fields as document ID, revision information and deletion status (_deleted) are required.\n\n```python\n\'\'\'\ndescription:\n    bulk docs function creates a documents or \n    updates existing documents by \n    providing the ids and revs of specific documents\n\nparameters:\n    docs: list[Union[BaseModel, dict]],\n    new_edits: None | bool = None\n\nreturns:\n    list[dict]\n\'\'\'\n\ndoc1: dict = {\'id\': user1._id, \'rev\': user1.rev}\n\n# updates/creates models by given list of dicts\n# with keys id and rev for specific document\nuser0_1: list[dict] = (await User.bulk_docs(list[doc1])).unwrap()\n```\n\n## Attachment\n\n### create/add attachment\nUploads the supplied content as an attachment to\nthe specified document.\nIf case when uploading an attachment using\nan existing attachment name,\nCouchDB will update the corresponding stored content of the database.\nSince you must supply the revision information to add an attachment to the document, this serves as validation to update the existing attachment.\n\n```python\n\'\'\'\ndescription:\n    add attachment function creates/adds attachment\n    to specific existing document in database\n    by providing attachment name (filename) and body as bytes\n\nparameters:\n    attachment_name: str,\n    body: bytes\n\nreturns:\n    tuple[BaseModel, CouchAttachment]\n\'\'\'\n\n# adds/creates attachment to specific document into database by given attachment name and body\ndata_tuple: tuple[BaseModel, CouchAttachment] = (\n            await user1.add_attachment(attachment_name = \'file_name\', body = content)).unwrap()\n```\n\n### get attachment\nReturns the file attachment associated with the document.\nThe raw data of the associated attachment is returned \n(just as if you were accessing a static file.\nThe returned Content-Type will be the same as the content\ntype set when the document attachment was submitted \ninto the database.\n```python\n\'\'\'\ndescription:\n    get attachment function gets the attachment\n    for specific existing document from database\n    by providing attachment name and range\n\nparameters:\n    attachment_name: str,\n    range: str | None = None\n\nreturns:\n    CouchAttachment\n\'\'\'\n\n# gets the attachment from database by name\nattachment: CouchAttachment = (\n            await user1.get_attachment(attachment_name = \'file_name\')).unwrap()\n```\n\n### update attachment\n```python\n\'\'\'\ndescription:\n    update attachment function updates attachment\n    for specific existing document from database\n    by providing attachment name (filename) and body\n\nparameters:\n    attachment_name: str,\n    body: bytes\n\nreturns:\n    tuple[BaseModel, CouchAttachment]\n\'\'\'\n\n# updates the attachment for specific document from database by attachment name and body\ndata_tuple: tuple[BaseModel, CouchAttachment] = (\n            await user1.update_attachment(attachment_name = \'file_name\', body = content)).unwrap()\n```\n\n### remove attachment\nDeletes the attachment with filename {attname} of the specified doc. You must supply the rev query parameter\nor If-Match with the current revision to\ndelete the attachment.\n\n```python\n\'\'\'\ndescription:\n    remove attachment function removes/deletes attachment\n    for specific existing document from database\n    by providing attachment name and range\n\nparameters:\n    attachment_name: str,\n    batch: None | str = None\n\nreturns:\n    BaseModel\n\'\'\'\n\n# removes/deletes the attachment for specific document from database by attachment name\ndata_tuple: BaseModel= (\n            await user1.remove_attachment(attachment_name = \'file_name\')).unwrap()\n```\n\n## Index\n### setup\n```python\n\'\'\'\ndescription:\n    load Index type from file using CouchLoader\n\nreturns:\n    BaseIndex\n\'\'\'\n\n# load Index type from file using CouchLoader\nUserIndex: type = loader.UserIndex_email_usertype\n```\n\n### create/add index\n```python\n\'\'\'\ndescription:\n    create index function creates/adds index\n    with specific fields into database\n    by providing ddoc as id/name, partial_filter_selector and partitioned\n\nparameters:\n    ddoc: Optional[str] = None,\n    partial_filter_selector: Optional[dict] = None,\n    partitioned: Optional[bool] = None\n\nreturns:\n    BaseIndex\n\'\'\'\n\n# creates/adds index with specific fields into database\nindex_: UserIndex = (await UserIndex.create()).unwrap()\n```\n\n### get indexes\nWhen you make a GET request to /db/_index, you get a list of all indexes in the database. In addition to the information available through this API, indexes are also stored in design documents <index-functions>. Design documents are regular documents that have an ID starting with _design/. Design documents can be retrieved and modified in the same way as any other document\n```python\n\'\'\'\ndescription:\n    get index function gets list of indexes from database\n\nreturns:\n    list[BaseIndex]\n\'\'\'\n \n# gets list of indexes from database\nindex_list: list[UserIndex] = (await UserIndex.get()).unwrap()\n```\n\n### update index\n```python\n\'\'\'\ndescription:\n    update index function updates specific index from database\n    by providing ddoc as id/name\n\nparameters:\n    ddoc: Optional[str] = None,\n    partial_filter_selector: Optional[dict] = None,\n    partitioned: Optional[bool] = None\n\nreturns:\n    BaseIndex\n\'\'\'\n\n# load Index type from file\nUserIndex: type = loader.UserIndex_email_usertype\n\n# update fields \nUserIndex.fields = [\'email\']\n\n# update index by given ddoc/name/id\nupdated_index = (await UserIndex.update(ddoc = \'ddoc\')).unwrap()\n```\n\n### delete index\n```python\n\'\'\'\ndescription:\n    delete index function deletes specific index from database\n    by providing designdoc as name/id\n\nparameters:\n    designdoc: Optional[str] = None\n\nreturns:\n    bool\n\'\'\'\n\n# delete index by given designdoc/name/id\ndeleted_index: bool = (await UserIndex.delete(designdoc = \'ddoc\')).unwrap()\n```\n\n## Object\n### setup\n```python\n\'\'\'\ndescription:\n    load Object type from file using CouchLoader\n    create instance of BaseObject\n\nreturns:\n    BaseObject\n\'\'\'\n\n# load Object type from file\nAgentProfile: type = loader.AgentProfile\n\n# create instance of BaseObject\nagent_profile = AgentProfile(x = 1)\n```\n\n ### create\n```python\n\'\'\'\ndescription:\n    creates instance of BaseModel, BaseObject\n    add function creates document into database\n    BaseModel type/document has BaseObject type attribute\n    call on model or model instance\n\n    if call on model:\n        parameters:\n            self: BaseModel\n\nreturns:\n    BaseModel\n\'\'\'\n\n# load Object type from file\nAgentProfile: type = loader.AgentProfile\n\n# create instance of AgentProfile/BaseObject\nagent_profile1_0: AgentProfile = AgentProfile(x = 1)\n\n# load Model type from file\nProfile: type = loader.Profile\n\n# create Profile/BaseModel object\n# BaseModel type/document has BaseObject type attribute\nprofile0: Profile = Profile(agent_profile = agent_profile1_0)\n\n# save model instance to database - call on model\nprofile1_0: Profile = (await Profile.add(profile0)).unwrap()\n\n# save model instance to database - call on model instance\nprofile1_0: Profile = (await profile0.add()).unwrap()\n```\n\n ### get\n```python\n\'\'\'\ndescription:\n    get function gets document from database\n    BaseModel type/document has BaseObject type attribute\n    by given document id and document rev\n\nparameters:\n    docid: str,\n    rev: None | str = None\n\nreturns:\n    BaseModel\n\'\'\'\n\n# get model from database by given id and rev, if rev is not passed document will be latest\n# BaseModel type/document has BaseObject type attribute\nprofile1_0: Profile = (await Profile.get(docid = profile0._id, rev = profile0._rev)).unwrap()\n\n# geting BaseObject type from model\nagent_profile1_1: AgentProfile = profile1_0.agent_profile\n```\n\n ### update\n```python\n\'\'\'\ndescription:\n    update function updates existing document \n    from database \n    BaseModel type/document has BaseObject type attribute\n    by providing fields to update\n\nparameters:\n    doc: dict, \n    batch: None | str = None, \n    new_edits: None | bool = None\n\nreturns:\n    BaseModel\n\'\'\'\n\n# geting BaseObject type from model\nagent_profile0: AgentProfile = profile0.agent_profile\n\n# change object\'s attribute\nagent_profile0.x = 10\n\ndoc_update: dict = {\n    \'agent_profile\': agent_profile0\n}\n\n# update model instance from database with given dict(keys as attributes)\nprofile0_1: Profile = (await profile0.update(doc = doc_update)).unwrap()\n```\n\n### delete\n```python\n\'\'\'\ndescription:\n    delete BaseObject type can be done in two ways:\n    - if field is not required, could be set to None, \n    and update BaseModel\n    - delete BaseModel type from database\n\nparameters:\n    if updating BaseModel:\n        doc: dict, \n        batch: None | str = None, \n        new_edits: None | bool = None\n    if deleting BaseModel:\n        batch: None | str = None\n\nreturns:\n    BaseModel\n\'\'\'\n\n# delete BaseObject type can be done in two ways\n\n# 1st \n# if agent_profile field is not required, could be set to None\ndoc_update: dict = {\n    \'agent_profile\': None\n}\n\n# update model instance from database with given dict\nprofile0_1: Profile = (await profile0.update(doc = doc_update)).unwrap()\n\n# 2nd\n# delete BaseModel type from database\nprofile0_1: Profile = (await profile0.delete()).unwrap()\n```\n\n<!-- Links -->\n\n<!-- Badges -->\n[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg\n[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause\n[build-image]: https://img.shields.io/badge/build-success-brightgreen\n[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green\n\n[pypi-project-url]: https://pypi.org/project/thcouch/\n[stable-ver-image]: https://img.shields.io/pypi/v/thcouch?label=stable\n[python-ver-image]: https://img.shields.io/pypi/pyversions/thcouch.svg?logo=python&logoColor=FBE072\n[status-image]: https://img.shields.io/pypi/status/thcouch.svg\n\n\n\n',
    'author': 'TangledHub',
    'author_email': 'info@tangledgroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tangledlabs/thcouch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
