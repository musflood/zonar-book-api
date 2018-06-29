# Design and Technology Choices

Due to the simplicity of the application, Pyramid was chosen over Django, as it is much more light-weight. While this resulted in the loss of the structure from class based views, splitting the view functions into delegated private functions for each of the HTTP methods allows ease of refactoring if necessary.

The endpoints for this API are limited to only two for the book wish list in order to make this API as RESTful as possible. In the same vein, each endpoint allows multiple HTTP methods, thus using various HTTP methods on the same endpoint will produce different results.

In order to control access to the books themselves, an owner is assigned to a Book when it is created in the form of a User. Once a book has been assigned an owner, it can only be accessed by that owner for viewing, updating, or deleting. This ensures the security of the books from other users. Also, requiring a user's email and password for every request ensures a level of statelessness in the server.

Pytest was used for testing as the use of fixtures with a variety of scopes was very useful for testing this API. For example, each User must have it's password hashed when it is created, which causes tests where a User is created to take a longer period of time. By using a module scoped fixture, a single User could be used for each testing module to keep testing time down.