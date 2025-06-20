import pstats

p = pstats.Stats('profile_output.prof')
p.strip_dirs().sort_stats('cumulative')

with open('profiling_report.txt', 'w') as f:
    p.stream = f
    p.print_stats()
