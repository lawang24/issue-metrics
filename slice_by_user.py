"""
A module for converting individual GitHub issue metrics into aggregations by user.
"""

"""
Input: List of individual github prs
Output: None

Writes to the markdown file all the individual PRS
"""

from datetime import timedelta

def slice_pr_by_user(issues_with_metrics, file):

    print("slice pr being called")

    author_stats = {}

    for issue in issues_with_metrics:

        author = issue.author

        if author not in author_stats:
            author_stats[author] = {
                    "total_time_to_first_response": 0,
                    "total_time_to_close": 0,
                    "total_time_to_answer": 0,
                    "first_response_count": 0,
                    "close_count": 0,
                    "answer_count": 0,
                    "total_prs": 0
                }

        if issue.time_to_first_response:
            author_stats[author]["total_time_to_first_response"] += issue.time_to_first_response.total_seconds()
            author_stats[author]["first_response_count"]+=1

        if issue.time_to_close:
            author_stats[author]["total_time_to_close"] += issue.time_to_close.total_seconds()
            author_stats[author]["close_count"]+=1
             
        if issue.time_to_answer:
            author_stats[author]["total_time_to_answer"] += issue.time_to_answer.total_seconds()
            author_stats[author]["answer_count"]+=1
        
        author_stats[author]["total_prs"] += 1
            

    columns = ["Author","Avg Time to First Response", "Avg Time to Close", "Avg Time to Answer", "Total PRs"]

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

        average_time_to_first_response = timedelta(seconds=stats["total_time_to_first_response"] // stats["first_response_count"]) if stats["first_response_count"] else "None"
        average_time_to_close = timedelta(seconds=stats["total_time_to_close"] // stats["close_count"]) if stats["total_time_to_close"] else "None"
        average_time_to_answer = timedelta(stats["total_time_to_answer"] // stats["answer_count"]) if stats["answer_count"] else "None"   
        total_prs = stats["total_prs"]
        
        file.write(f" {author} |")
        file.write(f" {average_time_to_first_response} |")
        file.write(f" {average_time_to_close} |")
        file.write(f" {average_time_to_answer} |")
        file.write(f" {total_prs} |")

        file.write("\n")
        
    file.write("\n")

