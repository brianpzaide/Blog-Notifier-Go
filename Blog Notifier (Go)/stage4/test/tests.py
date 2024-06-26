import multiprocessing
from .blognotifier_test_utils import *

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test


class TestBlogNotifierCLI(StageTest):

    @dynamic_test
    def test1_migrate_command(self):
        # Test the --migrate sub-command which creates the blogs.sqlite3 database and tables
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate").strip().lower()

        for table_name in tables_properties:
            if check_table_exists(table_name) is False:
                raise CheckResult.wrong(f"The --migrate command did not create the '{table_name}' table.")
            temp = check_table_properties(table_name)
            if temp[0] is False:
                raise CheckResult.wrong(
                    f"Wrong column types for '{table_name}' table."
                    f"\nExpected column types for the '{table_name}' table are {tables_properties[table_name]}."
                    f"\nFound: {temp[1]}")

        return CheckResult.correct()

    @dynamic_test
    def test2_explore_command(self):
        # Test the --list sub-command which lists all blog sites in the watch list
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_1 = blog_files[FLAT_MULTIPLE_LINKS_TEST][0]
        program.start('--explore', blog_1)
        program = TestedProgram()
        blog_2 = blog_files[FLAT_MULTIPLE_LINKS_TEST][1]
        program.start('--explore', blog_2)
        program = TestedProgram()
        blog_3 = blog_files[FLAT_MULTIPLE_LINKS_TEST][2]
        program.start('--explore', blog_3)
        program = TestedProgram()
        output = program.start("--list").strip()

        if f"{blog_1} {blog_1}" not in output or f"{blog_2} {blog_2}" not in output or f'{blog_3} {blog_3}' not in output:
            raise CheckResult.wrong(f"The --list command did not list all the blog sites in the watch list correctly."
                                    f"May be '--explore' functionality is not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test3_remove_command(self):
        # Test the --remove sub-command which removes a blog from the watch list
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_1 = blog_files[FLAT_MULTIPLE_LINKS_TEST][0]
        program.start('--explore', blog_1)
        program = TestedProgram()
        blog_2 = blog_files[FLAT_MULTIPLE_LINKS_TEST][1]
        program.start('--explore', blog_2)
        program = TestedProgram()
        program.start('--remove', blog_1).strip()

        program = TestedProgram()
        output = program.start("--list").strip()

        if f"{blog_1} {blog_1}" in output:
            raise CheckResult.wrong(
                "The --list command shows wrong output, seams like '--remove' flag was not implemented correctly")

        if f"{blog_2} {blog_2}" not in output:
            raise CheckResult.wrong(
                "The --list command shows wrong output, seams like '--remove' flag was not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test4_crawling_with_no_hyperlinks(self):
        # Test the crawl flag and list-posts sub-command.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', blog_files[NO_LINKS_TEST])
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog_files[NO_LINKS_TEST])

        output.strip()

        # Expected links from the example output
        expected_output = ""

        # Check if all expected links are present in the output
        if expected_output != output:
            return CheckResult.wrong(
                f"Wrong output for the test case: blog-site that has no blog-posts(no hyperlinks)"
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test5_crawling_with_nested_links_a(self):
        # Test the crawl flag and list-posts sub-command for blog with one blog-posts.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[NESTED_LINKS_TEST_1][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        output.strip()

        # Expected links from the example output
        expected_output = blog_files[NESTED_LINKS_TEST_1][0]

        # Check if all expected links are present in the output
        if expected_output not in output:
            return CheckResult.wrong(
                f"Test was carried out for blog site with just one blog post" 
                f"\nExpected_output: {expected_output} \nYour program output: {output}")

        return CheckResult.correct()

    @dynamic_test
    def test6_crawling_with_nested_links_b(self):
        # Test the crawl flag and list-posts sub-command for blog with 2 nested blog-posts.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[NESTED_LINKS_TEST_2][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        output.strip()

        # Expected links from the example output
        expected_output = blog_files[NESTED_LINKS_TEST_2][:-1]

        # Check if all expected links are present in the output
        for link in expected_output:
            if link not in output:
                return CheckResult.wrong(f"Test was carried out for site with nested links of depth 2"
                                         f"for example: a.html has link for b.html and b.html has link for c.html."
                                         f"your program must discover b.html and c.html"
                                         f"\nYour program output: {output}"
                                         f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test7_crawling_with_flat_multiple_pages(self):
        # Test the crawl flag and list-posts sub-command for blog with many blog-posts.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[FLAT_MULTIPLE_LINKS_TEST][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        output.strip()

        # Expected links from the example output
        expected_output = blog_files[FLAT_MULTIPLE_LINKS_TEST][:-1]

        # Check if all expected links are present in the output
        for link in expected_output:
            if link not in output:
                return CheckResult.wrong(
                    f"Test was carried out for blog site with multiple blog posts."
                    f"Your program did not discover all the links"
                    f"\nYour program output: {output}"
                    f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test8_crawling_with_nested_and_flat_posts(self):
        # Test the crawl flag and list-posts sub-command for blog with many blog-posts (flat and nested).
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[NESTED_AND_FLAT_LINKS_TEST][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        # Expected links from the example output
        expected_links = blog_files[NESTED_AND_FLAT_LINKS_TEST][:-1]

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in output:
                return CheckResult.wrong(
                    f"Test was carried out for blog site with multiple blog posts that may be flat or nested."
                    f"Your program did not discover all the links"
                    f"\nYour program output: {output}"
                    f"\nExpected links: {expected_links}")

        return CheckResult.correct()


@dynamic_test
def test9_crawling_and_update_last_link(self):
    # Test the crawl flag and checking if the last_link column of the blogs table is updated.
    remove_db_file()
    program = TestedProgram()
    program.start("--migrate")
    program = TestedProgram()
    blog = blog_files[FLAT_MULTIPLE_LINKS_TEST][-1]
    program.start('--explore', blog)
    program = TestedProgram()
    program.start("--crawl")

    program = TestedProgram()
    output = program.start("--list")

    output.strip()

    # Check if all expected links are present in the output
    for link in blog_files[FLAT_MULTIPLE_LINKS_TEST][:-1]:
        if f'{blog} {link}' in output:
            return CheckResult.correct()

    return CheckResult.wrong(
        f"Test was carried out for blog site with multiple blog posts,"
        f"The last_link column in the 'blogs' table is not updated.")


# Run the tests
if __name__ == '__main__':
    http_server_process: multiprocessing.Process = None
    try:
        # creating fake blog(just html files) for testing
        create_blog_site_with_no_posts()
        create_blog_site_with_nested_posts(1, NESTED_LINKS_TEST_1)
        create_blog_site_with_nested_posts(2, NESTED_LINKS_TEST_2)
        create_flat_blog_site_with_multiple_posts()
        create_blog_site_with_nested_and_flat_posts()
        # starting python's http.server
        http_server_process = multiprocessing.Process(target=run_http_server, args=(8000,))
        http_server_process.start()
        # running tests
        TestBlogNotifierCLI().run_tests()
    finally:
        # stopping python's http.server
        http_server_process.kill()
        # removing all the html files created
        remove_fake_blog()
