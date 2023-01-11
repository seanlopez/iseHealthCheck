test_list = ['Database Listener                      running          128286      \r', 'Database Server                        running          84 PROCESSES\r', 'Application Server                     running          142684      \r', 'Profiler Database                      running          135465      \r', 'ISE Indexing Engine                    running          144043      \r', 'AD Connector                           running          145196      \r', 'M&T Session Database                   running          135220      \r', 'M&T Log Processor                      running          171558      \r', 'Certificate Authority Service          running          145053      \r', 'EST Service                            running          167133      \r', 'SXP Engine Service                     disabled                     \r']

from ise_show_format import format_handler

format_processor = format_handler(test_list)
print(format_processor.format_application_info())
