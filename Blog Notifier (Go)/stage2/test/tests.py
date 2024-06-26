import os, sqlite3, random

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test, WrongAnswer

DB_FILE = 'blogs.sqlite3'

tables_properties = {
    'blogs': {
        'site': 'TEXT',
        'last_link': 'TEXT'
    },
    'posts': {
        'link': 'TEXT',
        'site': 'TEXT'
    },
    'mails': {
        'id': 'INTEGER',
        'mail': 'TEXT',
        'is_sent': 'INTEGER'
    }
}

def check_table_exists(table_name: str)-> bool:
    connection = sqlite3.connect(DB_FILE)  # Replace 'your_database.db' with your database file
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    # Fetch the result
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


def check_table_properties(table_name)-> tuple:
    # Connect to the SQLite database
    connection = sqlite3.connect(DB_FILE)  # Replace 'your_database.db' with your database file
    # Create a cursor object
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    # Fetch all the rows from the result
    columns_info = cursor.fetchall()
    columns_info = {column[1]:column[2] for column in columns_info}
    cursor.close()
    connection.close()
    return (tables_properties[table_name] == columns_info, columns_info)


def generate_random_blog_url()->str:
    temp = "".join(random.choices("abcdefghijklmnopqrstuvwxyz123456789", k = 12))
    blog_url = f'https://{temp}/blog'
    return blog_url


class TestBlogNotifierCLI(StageTest):

    @staticmethod
    def remove_db_file():
        print(os.curdir)
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    @dynamic_test
    def test1_migrate_command(self):
        self.remove_db_file()
        # Test the --migrate sub-command which creates the blogs.sqlite3 database and tables
        program = TestedProgram()
        output = program.start("--migrate").strip().lower()

        if "database 'blogs.sqlite3' created successfully" not in output:
            raise WrongAnswer("The --migrate command did not report successful creation of the database.")

        if "tables 'blogs', 'posts', and 'mails' initialized" not in output:
            raise WrongAnswer("The --migrate command did not report successful initialization of the tables.")

        for table_name in tables_properties:
            if check_table_exists(table_name) is False:
                raise WrongAnswer(f"The --migrate command did not create the '{table_name}' table.")
            temp = check_table_properties(table_name)
            if temp[0] is False:
                raise WrongAnswer(f"Wrong column types for '{table_name}' table. Expected column types for the '{table_name}' table are {tables_properties[table_name]}. Found {temp[1]}")

        return CheckResult.correct()

    @dynamic_test
    def test2_explore_command(self):
        self.remove_db_file()
        # Test the --explore sub-command which adds a new blog to the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        output = program.start('--explore', 'https://hyperskill.org/blog/').strip()

        if "New blog added to watchlist" not in output:
            raise WrongAnswer("The --explore command did not report adding a new blog to the watch list.")

        if "site: https://hyperskill.org/blog/" not in output or "last link: https://hyperskill.org/blog/" not in output:
            raise WrongAnswer("The --explore command did not output the correct blog information.")

        return CheckResult.correct()

    @dynamic_test
    def test3_explore_command_random(self):
        self.remove_db_file()
        # Test the --explore sub-command which adds a new blog to the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_url = generate_random_blog_url()
        output = program.start('--explore', blog_url).strip()

        if "New blog added to watchlist" not in output:
            raise WrongAnswer("The --explore command did not report adding a new blog to the watch list.")

        if f"site: {blog_url}" not in output or f"last link: {blog_url}" not in output:
            raise WrongAnswer("The --explore command did not output the correct blog information.")

        return CheckResult.correct()

    @dynamic_test
    def test4_edge_cases_explore_command(self):
        self.remove_db_file()
        # Test the --explore sub-command which adds a blog to the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', 'https://blog1.com')
        program = TestedProgram()
        output = program.start('--explore', 'https://blog1.com').strip()

        if "https://blog1.com already exists in the watch list" not in output:
            raise WrongAnswer("The --explore command did not report the correct message on adding a blog that is already in the watch list.")

        return CheckResult.correct()

    @dynamic_test
    def test5_edge_cases_explore_command_random(self):
        self.remove_db_file()
        # Test the --explore sub-command which adds a blog to the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_url = generate_random_blog_url()
        program.start('--explore', blog_url)
        program = TestedProgram()
        output = program.start('--explore', blog_url).strip()

        if f"{blog_url} already exists in the watch list" not in output:
            raise WrongAnswer("The --explore command did not report the correct message on adding a blog that is already in the watch list.")

        return CheckResult.correct()

    @dynamic_test
    def test6_list_command(self):
        self.remove_db_file()
        # Test the --list sub-command which lists all blog sites in the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore','https://blog1.com')
        program = TestedProgram()
        program.start('--explore','https://blog2.com')
        program = TestedProgram()
        blog_url = generate_random_blog_url()
        program.start('--explore', blog_url)
        program = TestedProgram()
        output = program.start("--list").strip()

        if "https://blog1.com https://blog1.com" not in output or "https://blog2.com https://blog2.com" not in output or f'{blog_url} {blog_url}' not in output:
            raise WrongAnswer("The --list command did not list all the blog sites in the watch list correctly.")

        return CheckResult.correct()

    @dynamic_test
    def test7_update_last_link_command(self):
        self.remove_db_file()
        # Test the --update-last-link sub-command which updates the last link of a blog site
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', 'https://blog1.com')
        program = TestedProgram()
        output = program.start('update-last-link', '--site', 'https://blog1.com', '--post', 'https://blog1.com/post200').strip()

        if "The last link for https://blog1.com updated to https://blog1.com/post200" not in output:
            raise WrongAnswer("The --update-last-link command did not report the correct update message.")

        program = TestedProgram()
        output = program.start("--list").strip().lower()

        if "https://blog1.com https://blog1.com/post200" not in output:
            raise WrongAnswer("The --list command shows wrong output, seams that 'update-last-link' sub-command was not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test8_update_last_link_command_random(self):
        self.remove_db_file()
        # Test the --update-last-link sub-command which updates the last link of a blog site
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_url = generate_random_blog_url()
        program.start('--explore', blog_url)
        program = TestedProgram()
        output = program.start('update-last-link', '--site', blog_url, '--post', f'{blog_url}/post101').strip()

        if f"The last link for {blog_url} updated to {blog_url}/post101" not in output:
            raise WrongAnswer("The --update-last-link command did not report the correct update message.")

        program = TestedProgram()
        output = program.start("--list").strip().lower()

        if f"{blog_url} {blog_url}/post101" not in output:
            raise WrongAnswer("The --list command shows wrong output, seams that 'update-last-link' sub-command was not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test9_remove_command(self):
        self.remove_db_file()
        # Test the --remove sub-command which removes a blog from the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', 'https://blog1.com')
        program = TestedProgram()
        output = program.start('--remove', 'https://blog1.com').strip()

        if "https://blog1.com removed from the watch list." not in output:
            raise WrongAnswer("The --remove command did not report the correct removal message.")

        program = TestedProgram()
        output = program.start("--list").strip()

        if "https://blog1.com https://blog1.com" in output:
            raise WrongAnswer("The --list command shows wrong output, seams that '--remove' flag was not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test10_remove_command_random(self):
        self.remove_db_file()
        # Test the --remove sub-command which removes a blog from the watch list
        program = TestedProgram()
        program.start("--migrate")
        blog_url = generate_random_blog_url()
        program = TestedProgram()
        program.start('--explore', blog_url)
        program = TestedProgram()
        output = program.start('--remove', blog_url).strip()

        if f"{blog_url} removed from the watch list." not in output:
            raise WrongAnswer("The --remove command did not report the correct removal message.")

        program = TestedProgram()
        output = program.start("--list").strip()

        if f"{blog_url} {blog_url}" in output:
            raise WrongAnswer("The --list command shows wrong output, seams that '--remove' flag was not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test11_edge_cases_remove_command(self):
        # Test edge cases like removing a non-existent blog site
        program = TestedProgram()
        program.start("--migrate")
        blog_url = generate_random_blog_url()
        program = TestedProgram()
        output = program.start('--remove', blog_url).strip()

        if f"{blog_url} does not exist in the watch list" not in output:
            raise WrongAnswer("The --remove command did not handle non-existent blog sites correctly.")

        return CheckResult.correct()


if __name__ == '__main__':
    TestBlogNotifierCLI().run_tests()
