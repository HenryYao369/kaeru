Managing the Back End:

1. Models - all data models are in kaeru/models.py. The three models that are currently set up are:
		Projects (for managing the permissions for and organization of a set of pages)
		Pages (pages that are served for public viewing)
		Code (for the code that is served for a page)

2. Urls - there are several urls in urls.py dedicated for interacting with the back end. The main ones are:
		pages/<user>/<project>/<page>/ (for public viewing of a developer's served page)
		projects/<user>/ (for viewing and managing a developer's projects)
		projects/<user>/<project>/ (for viewing and managing a specific project)
		projects/<user>/<project>/<page> (for viewing and managing a specific page of a project)

3. Views - the views in kaeru/views.py are the main functions responsible for serving the responses to requests. The two functions used mainly for interacting with the back end are:
		projects_view (for viewing and managing a developer's pages and projects)
		pages_view (for serving a developer's page to the public)
	Additionally, there are several HTML templates used when processing the responses. The ones referenced in the above two functions are:
		404.html (for when a given user, project, or page is not found)
		private.html (for when the logged in user has no permission to view a project)
		projects.html (for viewing all of a developer's projects)
		project.html (for viewing and managing a specific project)
		pages.html (for viewing and managing a specific page)
		page.html (for serving a specific page)

4. Utils - views also make calls to functions in kaeru/utils.py in order to handle various POST requests. These dedicated functions are: 
		handler_user_post (for adding and removing a user's projects)
		handle_project_post (for changing contents and settings for a project)
		handle_page_post (for changing contents for a page)
	Each one takes in an operation name and arguments for the operation, specifics are documented for each one in utils.py.

5. Tests - there are dedicated tests in tests.py in order to test all of the above functionality:
		test_create_project_view (for testing functionality of creating, managing, and viewing projects)
		test_create_pages_view (for testing functionality of creating, managing, and viewing pages)
		test_create_code_view (for testing functionality of managing code for pages)
		test_contributors_view (for testing functionality of project and page permissions)