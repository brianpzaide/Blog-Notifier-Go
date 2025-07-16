# Blog-Notifier

Blog-Notifier is a command-line tool built for the Go track on [Hyperskill](https://hyperskill.org). It helps users keep track of their favorite blogs by sending an email notification whenever a new post is published. Users can add or remove blogs from their personal watchlist.

## Project Description

The project is built in five stages, with each stage adding new functionality:

### Stage 1 - Config File Support
Set up a basic CLI that can read configuration settings from a YAML file. This allows the Blog Notifier to load email and server settings dynamically, so the app can be configured without changing the code.

### Stage 2 – Manage Blog Watchlist
Add functionality to let users create and manage a watchlist of their favorite blogs. Users should be able to add, update, or remove blog sites from the list using the CLI.

### Stage 3 – Website Crawler
Add functionality to recursively crawl a blog website up to a specified depth. The CLI should collect all discovered links and display them in a clear, user-friendly format.

### Stage 4 – Monitor Blogs for Updates
Add functionality to crawl all blogs in the watchlist and check for new posts. The CLI should update the local database with any new entries it finds, so that the watchlist up to date with the latest content.

### Stage 5 – Email Notifications
Add functionality to notify users by email when new blog posts are found on sites in their watchlist. This completes the core functionality of the Blog Notifier by keeping users updated in real time.

## Learning Outcomes

Working on this project offers valuable hands-on experience with a range of essential Go skills, including:
- Parsing and working with YAML configuration files.
- Building a recursive website crawler.
- Sending emails programmatically.
- Using Go’s concurrency features effectively.
- Performing CRUD (Create, Read, Update, Delete) operations on data.

## Feedback and Contributions
Blog Notifier is in active development. Feedback, suggestions, and pull requests are welcome. Feel free to check out the project [here](https://hyperskill.org/projects/437) and contribute to its improvement.
