"""
A module for converting individual GitHub issue metrics into aggregations by user.
"""

"""
Input: List of individual github prs
Output: None

Writes to the markdown file all the individual PRS
"""

import json

def slice_pr_by_user(issues_with_metrics):

    author_stats = {}

    for issue in issues_with_metrics:
        print(json.dumps(issue))

        author = issue.author
        time_to_first_response = int(issue.time_to_first_response)
        time_to_close = int(issue.time_to_close)
        time_to_answer = int(issue.time_to_answer)

        if author in author_stats:
            # Update total time and count for this author for each metric
            author_stats[author]["total_time_to_first_response"] += time_to_first_response
            author_stats[author]["total_time_to_close"] += time_to_close
            author_stats[author]["total_time_to_answer"] += time_to_answer
            author_stats[author]["count"] += 1
        else:
            # Initialize this author's stats with all necessary metrics
            author_stats[author] = {
                "total_time_to_first_response": time_to_first_response,
                "total_time_to_close": time_to_close,
                "total_time_to_answer": time_to_answer,
                "count": 1
            }

    columns = ["Title", "URL","Avg Time to First Response", "Avg Time to Close", "Avg Time to Answer"]

    with open("issue_metrics.md", "w", encoding="utf-8") as file:
        file.write("# User-Aggregated Metrics\n\n")

        # Write table with individual issue/pr/discussion metrics
        # First write the header
        file.write("|")
        for column in columns:
            file.write(f" {column} |")
        file.write("\n")

        # Then write the column dividers
        file.write("|")
        for _ in columns:
            file.write(" --- |")
        file.write("\n")
        
        # Then write the issues/pr/discussions row by row
        for author, stats in author_stats.items():

            average_time_to_first_response = stats["total_time_to_first_response"] / stats["count"]
            average_time_to_close = stats["total_time_to_close"] / stats["count"]
            average_time_to_answer = stats["total_time_to_answer"] / stats["count"]
            
            file.write(f" {author} |")
            file.write(f" {average_time_to_first_response} |")
            file.write(f" {average_time_to_close} |")
            file.write(f" {average_time_to_answer} |")
            file.write("\n")
        

