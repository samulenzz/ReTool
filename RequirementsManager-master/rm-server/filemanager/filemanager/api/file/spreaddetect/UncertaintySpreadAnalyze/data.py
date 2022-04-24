# remake/NlToList.py用，把条目化的自然语言需求放进来即可
Nl = [
    '项目打开时间功能能够支持打开模型数小于150个的项目的时间小于3秒。',
    '5.5.4	单视图结构下模型数量要求\n单个视图结构下可支持管理的模型数不少于40个。',
    '通用性能指标如表22所示。\n5.5.1	响应时间指标功能\n响应时间指标功能，用户页面响应时间一般不超过3秒。\n5.5.2	项目打开时间功能\n项目打开时间功能能够支持打开模型数小于150个的项目的时间小于3秒。',
]



# 非功能需求 remake/NlToList.py生成
testNf = [
    {'id': '0', 'description': '项目打开时间功能能够支持打开模型数小于150个的项目的时间小于3秒。'},
    {'id': '1', 'description': '5.5.4\t单视图结构下模型数量要求\n单个视图结构下可支持管理的模型数不少于40个。'},
    {'id': '2', 'description': '通用性能指标如表22所示。\n5.5.1\t响应时间指标功能\n响应时间指标功能，用户页面响应时间一般不超过3秒。\n5.5.2\t项目打开时间功能\n项目打开时间功能能够支持打开模型数小于150个的项目的时间小于3秒。'}
]

# 功能需求 FSARC-master/demo.py生成
testF = [
{'id':"4",'groupid':"0",'event':"",'agent':"[human]resource class",'operation':"have",'input':"[human]resource class, [resource]resource assignment, tasks",'output':"list",'restriction':"",'description':'''The human resource class can have multiple objects of resource assignments which assigns this resource to tasks. The class provides function to get the list of these objects.'''},

{'id':"10",'groupid':"0",'event':"",'agent':"[Using]gui user",'operation':"change",'input':"[Using]gui user, gui",'output':"the length of a task",'restriction':"'on the GUI'",'description':'''Using GUI user should be able to change the length of a task by dragging-and-dropping the bar on the GUI.'''},

{'id':"11",'groupid':"0",'event':"",'agent':"[Using]gui user",'operation':"change",'input':"[Using]gui user",'output':"the length of a task",'restriction':"'via date picker control'",'description':'''Using GUI user should be able to change the length of a task via date picker control.'''},

{'id':"13",'groupid':"0",'event':"",'agent':"class",'operation':"not",'input':"start date[of ], dependee task, end date[of ]",'output':"",'restriction':"'not'",'description':'''A class is used to represent the constraint that the start date of the dependee task should not be earlier than the end date of the dependent task.'''},

{'id':"25",'groupid':"0",'event':"{'agent': '[new]dependency' , 'operation': 'cause' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"[new]dependency",'operation':"cause",'input':"dependency collection, new dependency, dependency class",'output':"exception",'restriction':"",'description':'''The class of dependency collection provides a function to check if the new dependency will cause a loop each time a object of dependency class is created. The function returns an exception if there is a loop. '''},

{'id':"27",'groupid':"0",'event':"",'agent':"system",'operation':"evaluate",'input':"critical path",'output':"",'restriction':"",'description':'''The system should be able to evaluate critical path in a project.'''},

{'id':"40",'groupid':"0",'event':"{'agent': '.' , 'operation': 'when' , 'input': 'task, ganttproject class, gantttreetablenode, defaultmutabletreenode class' , 'output': 'task' , 'restriction': '*void*}",'agent':".",'operation':"when",'input':"*, ganttproject class, gantttreetablenode defaultmutabletreenode class",'output':"*",'restriction':"",'description':'''When deleting a task the GanttProject class calls GanttTreeTableNode and DefaultMutableTreeNode classes to identify the parent of the task being deleted.'''},

{'id':"41",'groupid':"0",'event':"{'agent': '.' , 'operation': 'deleting' , 'input'task' , 'output': 'task' , 'restriction': '*void*}",'agent':".",'operation':"calls",'input':"ganttproject class, AdjustTaskBoundsAlgorithm",'output':"*",'restriction':"",'description':'''When deleting a task the GanttProject class calls AdjustTaskBoundsAlgorithm and passes the parent of the deleted task as a parameter. The AdjustTaskBoundsAlgorithm takes care of handling and releasing resources associated with the deleted task. '''},

{'id':"42",'groupid':"0",'event':"",'agent':"gui",'operation':"change",'input':"task name",'output':"task name",'restriction':"",'description':'''GUI should able to provide ability to change task name. '''},

{'id':"43",'groupid':"0",'event':"",'agent':"gui",'operation':"change",'input':"start/end date of a task",'output':"start/end date of a task",'restriction':"",'description':'''GUI should able to provide ability to change start/end date of a task.'''},

{'id':"44",'groupid':"0",'event':"",'agent':"gui",'operation':"set",'input':"task",'output':"progress",'restriction':"",'description':'''GUI should able to provide ability to set progress on a task.'''},

{'id':"48",'groupid':"0",'event':"",'agent':"subtask gantttree2 class",'operation':"not",'input':"gantttree2 class, task node, [original]parent task[of original]",'output':"tasks as subtasks, relationship",'restriction':"'not'",'description':'''To remove tasks as subtasks GanttTree2 class calls a method which dedent selected task nodes in GUI so that they will not be subtasks of their original parents tasks. An object of a class is used to remove relationship between selected tasks and their original parents and add relationship between selected tasks and their new parents.'''},

{'id':"49",'groupid':"0",'event':"",'agent':"[which dedent selected task nodes in GUI so that they]method",'operation':"not",'input':"task node, task tree model, [original]parent task[of original]",'output':"relationship",'restriction':"'not'",'description':'''To remove tasks as subtasks a method which dedent selected task nodes in GUI so that they will not be subtasks of their original parents tasks is used. The task tree model provides methods to remove relationship between selected tasks and their original parents and add relationship between selected tasks and their new parents.'''},

{'id':"51",'groupid':"0",'event':"",'agent':"user",'operation':"create",'input':"",'output':"milestones",'restriction':"",'description':'''User should be able to create milestones.'''},

{'id':"52",'groupid':"0",'event':"",'agent':"user interface",'operation':"specify",'input':"user interface, a specific task, milestone",'output':"",'restriction':"",'description':'''User interface should be able to provide an ability to specify whether a specific task in a milestone.'''},

{'id':"53",'groupid':"0",'event':"",'agent':".",'operation':"display",'input':"*",'output':"*",'restriction':"'visually', 'differently'",'description':'''Milestone should be displayed visually differently from regular tasks.'''},

{'id':"67",'groupid':"0",'event':"",'agent':".",'operation':"capture",'input':"[two]tasks",'output':"dependency",'restriction':"",'description':'''The fact of linking of one task to another should be captured as dependency between two tasks.'''},

{'id':"68",'groupid':"0",'event':"{'agent': '[two][more]task' , 'operation': 'are link' , 'input': '[two][more]task' , 'output': '*void*' , 'restriction': '*void*}",'agent':"[two][more]task",'operation':"be check",'input':"tasks, link",'output':"potential collisions",'restriction':"",'description':'''When a two or more tasks are link, there should be check conducted for potential collisions on the chart.'''},

{'id':"69",'groupid':"0",'event':"",'agent':"start",'operation':"*",'input':"start and end dates for the graph",'output':"*",'restriction':"",'description':'''The start and end dates for the graph can be either flexible or rigid for the purpose of adjusting and fixing potential collisions. '''},

{'id':"76",'groupid':"0",'event':"",'agent':"spacecraftindicator verification",'operation':"write",'input':"Log_messages, spacecraft_indicator verification",'output':"Level0_header_log_msgs",'restriction':"",'description':'''Shall write Level0_header_log_msgs to Log_messages if the Spacecraft_indicator verification fails.  '''},

{'id':"79",'groupid':"0",'event':"{'agent': '.' , 'operation': 'read' , 'input': 'modispackets' , 'output': 'modispackets' , 'restriction': 'not}",'agent':"modispackets",'operation':"issue",'input':"MODIS_packets, level0data file",'output':"Program_stop",'restriction':"'not'",'description':'''Shall issue Program_stop if MODIS_packets cannot be read from Level0_data file.  '''},

{'id':"82",'groupid':"0",'event':"",'agent':"algorithm",'operation':"calculate",'input':"an algorithm to be supplied by SBRS",'output':"packet checksum",'restriction':"",'description':'''Shall calculate the packet checksum using an algorithm to be supplied by SBRS.  '''},

{'id':"85",'groupid':"0",'event':"{'agent': 'packet' , 'operation': 'belong' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"packet",'operation':"determine",'input':"packet, scan",'output':"",'restriction':"",'description':'''Shall determine if the packet belongs in the current scan.  '''},

{'id':"87",'groupid':"0",'event':"{'agent': 'packet' , 'operation': 'miss' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"packet",'operation':"determine",'input':"packets, scan",'output':"",'restriction':"",'description':'''Shall determine if packets are missing from the current scan.  '''},

{'id':"88",'groupid':"0",'event':"{'agent': 'missing packets' , 'operation': 'detect' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"[missing]packet",'operation':"write",'input':"Log_messages",'output':"Missing_packet_log_msgs",'restriction':"",'description':'''Shall write Missing_packet_log_msgs to Log_messages when missing packets are detected.  '''},

{'id':"89",'groupid':"0",'event':"",'agent':"packet",'operation':"unpack",'input':"radiance data, MODIS_pkt, Unpacked_MODIS_radiance, format documented in SBRS CDRL 305",'output':"",'restriction':"'to UnpackedMODISradiance'",'description':'''Shall unpack all radiance data from 12-bits in the MODIS_pkt to Unpacked_MODIS_radiance when the packet contains radiance data, using the format documented in SBRS CDRL 305. '''},

{'id':"90",'groupid':"0",'event':"",'agent':"packet",'operation':"unpack",'input':"engineering or memory data, MODIS_pkt, Eng_Mem_data, format documented in SBRS CDRL 305",'output':"",'restriction':"'to EngMemdata'",'description':'''Shall unpack all engineering or memory data from the MODIS_pkt to Eng_Mem_data when the packet contains engineering or memory data, using the format documented in SBRS CDRL 305.   '''},

{'id':"91",'groupid':"0",'event':"",'agent':"create",'operation':"create",'input':"Level1A_data product, Level0_open_metadata, metadata contained in MODIS_scan",'output':"ECS_standard_global_metadata, MODISL1A_specific_global_metadata",'restriction':"",'description':'''Shall create ECS_standard_global_metadata and MODISL1A_specific_global_metadata for each completed Level1A_data product, using Level0_open_metadata and selected metadata contained in MODIS_scan.  '''},

{'id':"94",'groupid':"0",'event':"",'agent':"information",'operation':"unpack",'input':"Current_HK_telem, Prior_HK_telem, Sci_eng_data, format described in SBRS CDRL 305",'output':"information",'restriction':"",'description':'''Shall unpack the information contained in Current_HK_telem,  Prior_HK_telem, and Sci_eng_data, using the format described in SBRS CDRL 305.   '''},

{'id':"95",'groupid':"0",'event':"",'agent':"value",'operation':"update",'input':"values, Current_HK_telem, Prior_HK_telem, Sci_eng_data",'output':"Decommutated_eng_mem_list",'restriction':"",'description':'''Shall update Decommutated_eng_mem_list with the values extracted from Current_HK_telem, Prior_HK_telem, and Sci_eng_data'''},

{'id':"96",'groupid':"0",'event':"",'agent':"geolocation software",'operation':"follow",'input':"L1A/Geolocation software, coding standards, MODIS Software Development Standards and Guidelines",'output':"",'restriction':"",'description':'''The L1A/Geolocation software shall follow the coding standards established by the MODIS project in MODIS Software Development Standards and Guidelines  '''},

{'id':"97",'groupid':"0",'event':"",'agent':"geolocation software",'operation':"use",'input':"L1A/Geolocation software, mandatory SDPTK routines, additional SDPTK routines",'output':"",'restriction':"",'description':'''The L1A/Geolocation software shall use all applicable mandatory SDPTK routines and any additional SDPTK routines that are useful.  '''},

{'id':"98",'groupid':"0",'event':"",'agent':"geolocation software",'operation':"use",'input':"L1A/Geolocation software, HDF Version 4.1r1, HDF files",'output':"HDF files",'restriction':"",'description':'''The L1A/Geolocation software shall use HDF Version 4.1r1 for reading and writing all HDF files.  '''},

{'id':"99",'groupid':"0",'event':"{'agent': 'write' , 'operation': 'write' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"write error",'operation':"generate",'input':"write error",'output':"data_output_status_messages",'restriction':"",'description':'''Shall generate data_output_status_messages if write errors are encountered.  '''},

{'id':"100",'groupid':"0",'event':"{'agent': 'write' , 'operation': 'write' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"write error",'operation':"generate",'input':"write error",'output':"data_output_status_messages",'restriction':"",'description':'''Shall generate data_output_status_messages if write errors are encountered.  '''},

{'id':"102",'groupid':"0",'event':"",'agent':"[corrupt]convertedspacecraftancillarydata",'operation':"detect",'input':"corrupt converted_spacecraft_ancillary_data",'output':"validated_spacecraft_ancillary_data",'restriction':"",'description':'''Shall detect corrupt converted_spacecraft_ancillary_data to produce validated_spacecraft_ancillary_data.  '''},

{'id':"103",'groupid':"0",'event':"{'agent': '.' , 'operation': 'when' , 'input': '[corrupted]datum value' , 'output': '[corrupted]datum value' , 'restriction': '*void*}",'agent':"[corrupted]datum value",'operation':"generate",'input':"corrupted data values",'output':"data_input_status_messages",'restriction':"",'description':'''Shall generate data_input_status_messages when corrupted data values are detected.  '''},

{'id':"105",'groupid':"0",'event':"",'agent':"[corrupted]datum value",'operation':"generate",'input':"corrupted data values",'output':"data_input_status_messages, scan_quality_flags",'restriction':"",'description':'''Shall generate data_input_status_messages and set scan_quality_flags if corrupted data values are detected.  '''},

{'id':"110",'groupid':"0",'event':"{'agent': 'write' , 'operation': 'write' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"write error",'operation':"generate",'input':"write error",'output':"data_output_status_messages",'restriction':"",'description':'''Shall generate data_output_status_messages if write errors are encountered.  '''},

{'id':"111",'groupid':"0",'event':"{'agent': 'write' , 'operation': 'write' , 'input': '*void*' , 'output': '*void*' , 'restriction': '*void*}",'agent':"write error",'operation':"generate",'input':"write error",'output':"data_output_status_messages",'restriction':"",'description':'''Shall generate data_output_status_messages if write errors are encountered.  '''},

{'id':"112",'groupid':"0",'event':"{'agent': '.' , 'operation': 'encounter' , 'input': 'error' , 'output': 'error' , 'restriction': '*void*}",'agent':"error",'operation':"generate",'input':"Level_1B_Data",'output':"data_input_status_messages",'restriction':"",'description':'''Shall generate data_input_status_messages if errors are 	encountered in reading Level_1B_Data.  '''},

{'id':"113",'groupid':"0",'event':"{'agent': '.' , 'operation': 'encounter' , 'input': 'error' , 'output': 'error' , 'restriction': '*void*}",'agent':"error",'operation':"generate",'input':"Level_2_Data",'output':"data_input_status_messages",'restriction':"",'description':'''Shall generate data_input_status_messages if errors are encountered in reading Level_2_Data. '''},

{'id':"114",'groupid':"0",'event':"",'agent':"geolocation software",'operation':"generate",'input':"L1A/Geolocation software",'output':"initiation_messages",'restriction':"",'description':'''The L1A/Geolocation software shall generate initiation_messages at program commencement.  '''},

{'id':"115",'groupid':"0",'event':"",'agent':"geolocation software",'operation':"use",'input':"L1A/Geolocation software, mandatory SDPTK 5.2 routines, additional SDPTK routines",'output':"",'restriction':"",'description':'''The L1A/Geolocation software shall use all applicable mandatory SDPTK 5.2 routines and any additional SDPTK routines that are useful.  '''},

{'id':"117",'groupid':"0",'event':"",'agent':"there",'operation':"a",'input':"[single]entry point, libwarc",'output':"",'restriction':"",'description':'''There shall be a single entry point to libwarc, called "warc.h".'''},

{'id':"118",'groupid':"0",'event':"",'agent':".",'operation':"structure",'input':"libwarc header, warc.h",'output':"libwarc header",'restriction':"",'description':'''The libwarc headers shall be structured in a hierarchical manner. The universal header "warc.h" will include all of them.'''},

{'id':"119",'groupid':"0",'event':"",'agent':"it",'operation':"be possible",'input':"warc file format",'output':"WARC file format",'restriction':"'by'",'description':'''It shall be possible for developers to access, modify and manipulate of all aspects of the WARC file format by including this single header file.'''},

{'id':"120",'groupid':"0",'event':"",'agent':"[universal]header warc.h",'operation':"ensure",'input':"[universal]header warc.h, ALL version[of ]libwarc",'output':"",'restriction':"",'description':'''The universal header "warc.h" shall ensure compatibility between all versions of libwarc.'''},

{'id':"122",'groupid':"0",'event':"",'agent':"change",'operation':"ensure",'input':"interfaces in libwarc, library, tool or application based on libwarc",'output':"",'restriction':"'not'",'description':'''The interfaces in libwarc shall ensure that any changes to the library, will not affect any tool or application based on libwarc.'''},

{'id':"123",'groupid':"0",'event':"",'agent':"[universal]header warc.h",'operation':"provide",'input':"warc.h, ISO TC 46/SC 4 N 595, ",'output':"WARC-records, WARC records",'restriction':"",'description':'''The universal header "warc.h" shall provide normalised interfaces to enable developers to create valid and compliant WARC-records, based on the definition in the "ISO TC 46/SC 4 N 595" standards document. The interfaces shall be made available to create WARC records of the following types:- "warinfo"- "response"- "request"- "metadata"- "revisit"- "conversion"- "continuation"- "resource"'''},

{'id':"124",'groupid':"0",'event':"",'agent':"ALL warc record",'operation':"be accessible",'input':"WARC-record, peer C class",'output':"",'restriction':"'via a peer C class of the same name'",'description':'''Each WARC-record shall be accessible via a peer C class of the same name.'''},

{'id':"125",'groupid':"0",'event':"",'agent':"attribute[of ]",'operation':"have",'input':"WARC-record, ISO standard specification, peer C class",'output':"",'restriction':"",'description':'''The attributes of each WARC-record, as per the ISO standard specification, shall have a corresponding attribute in its peer C class.'''},

{'id':"126",'groupid':"0",'event':"",'agent':"ALL peer class",'operation':"expose",'input':"peer class, WARC-record",'output':"WARC-record",'restriction':"",'description':'''Each peer class shall expose a set a class functions to read, write, and update attributes for the corresponding WARC-record.'''},

{'id':"127",'groupid':"0",'event':"",'agent':"libwarc",'operation':"provide",'input':"data",'output':"API",'restriction':"",'description':'''Libwarc shall provide an API describing (1) the set of data, and (2) the set of operations that can be performed on the data. The data types shall be abstract (abstract data types - ADT), to ensure independence of concrete implementations.'''},

{'id':"128",'groupid':"0",'event':"",'agent':"it",'operation':"create",'input':"constructor",'output':"WARC-record, abstract handle",'restriction':"",'description':'''It shall be possible to create a WARC-record using a constructor, which will returns an abstract handle representing the WARC-record.'''},

{'id':"129",'groupid':"0",'event':"",'agent':"it",'operation':"be possible",'input':"destructor",'output':"WARC-record",'restriction':"",'description':'''It shall be possible to release the WARC-record using a destructor.'''},

{'id':"130",'groupid':"0",'event':"",'agent':"operation",'operation':"be possible",'input':"WARC-record, abstract handle",'output':"",'restriction':"",'description':'''Any operations on WARC-records shall be possible using functions accepting the abstract handle as an argument.'''},

{'id':"131",'groupid':"0",'event':"",'agent':"libwarc",'operation':"include to ADT objects to",'input':"adt object, ARC-records",'output':"",'restriction':"",'description':'''Libwarc shall include ADT objects to handle read operations on ARC-records'''},

{'id':"132",'groupid':"0",'event':"",'agent':"libwarc",'operation':"provide",'input':"WARCrecords",'output':"generic iterator, abstract WARC-document",'restriction':"",'description':'''Libwarc shall provide a generic iterator, to enable the developer to iterate over all WARCrecords and create an abstract WARC-document as a simple container'''},

{'id':"133",'groupid':"0",'event':"",'agent':"libwarc",'operation':"provide",'input':"WARC-record",'output':"iterator",'restriction':"",'description':'''Libwarc shall provide a WARC-record MIME-type iterator'''},

{'id':"134",'groupid':"0",'event':"",'agent':"libwarc",'operation':"provide",'input':"",'output':"WARC-record-type iterator",'restriction':"",'description':'''Libwarc shall provide a WARC-record-type iterator'''},

{'id':"135",'groupid':"0",'event':"",'agent':"purpose",'operation':"customise",'input':"generic iterators, callback handlers",'output':"generic iterators",'restriction':"'via callback handlers '",'description':'''Libwarc's generic iterators may be customised for different purposes via callback handlers (i.e. hooks)'''},

{'id':"136",'groupid':"0",'event':"",'agent':".",'operation':"combine",'input':"iterators",'output':"composite iterators",'restriction':"'more', ''",'description':'''Libwarc's iterators may be combined into composite iterators to enable the developer to more than one search field'''},

{'id':"137",'groupid':"0",'event':"",'agent':"libwarc",'operation':"encapsulate",'input':"WARCrecords",'output':"memory management",'restriction':"",'description':'''Libwarc shall encapsulate and handle all memory management when processing WARCrecords.'''},

{'id':"138",'groupid':"0",'event':"",'agent':".",'operation':"developer",'input':"constructor, destructor",'output':"memory",'restriction':"'not', 'directly', 'instead'",'description':'''Developers using libwarc shall not be required to allocate/release memory directly, instead the developer shall use libwarc's object constructor and destructor functions.'''},

{'id':"139",'groupid':"0",'event':"",'agent':"libwarc",'operation':"use",'input':"heap memory",'output':"",'restriction':"",'description':'''Libwarc shall use dynamic heap memory for its internal usage.'''},

{'id':"140",'groupid':"0",'event':"",'agent':"libwarc",'operation':"allocate to minimum memory heap to",'input':"WARC-record metadata",'output':"memory heap",'restriction':"",'description':'''Libwarc shall allocate minimum memory heap to store WARC-record metadata.'''},

{'id':"142",'groupid':"0",'event':"",'agent':"libwarc",'operation':"not",'input':"file to memory mapping technology",'output':"memory",'restriction':"'not', 'instead', 'explicitly'",'description':'''Libwarc shall not use file to memory mapping technology, instead libwarc will explicitly allocate memory as needed.'''},

{'id':"143",'groupid':"0",'event':"",'agent':"libwarc",'operation':"support",'input':"on-compressed WARC-records, compressed WARC-records, files",'output':"",'restriction':"",'description':'''Libwarc shall support non-compressed WARC-records and compressed WARC-records and files'''},

{'id':"144",'groupid':"0",'event':"",'agent':"default compression format",'operation':"be Gzip",'input':"default compression format",'output':"",'restriction':"",'description':'''The default compression format shall be Gzip'''},

{'id':"145",'groupid':"0",'event':"",'agent':"libwarc",'operation':"support",'input':"compression schemas, compressor",'output':"",'restriction':"",'description':'''Libwarc shall support multiple compression schemas, loading a specific compressor at runtime as an external shared library.'''},

{'id':"146",'groupid':"0",'event':"",'agent':"it",'operation':"not",'input':"compression schema, WARC file",'output':"",'restriction':"'not', 'more', 'within a single WARC file '",'description':'''It shall not be possible to use more than one compression schema (including noncompression) within a single WARC file. (i.e. it is not possible to mix compression schemes within a single WARC file).'''},

{'id':"147",'groupid':"0",'event':"",'agent':".",'operation':"implement",'input':"WARC-records, WARC ISO standard",'output':"command line tool",'restriction':"",'description':'''A command line tool shall be implemented utilising libwarc to check the consistency of WARC-records and their conformance to the WARC ISO standard.'''},

{'id':"148",'groupid':"0",'event':"",'agent':"line tool",'operation':"notify",'input':"command line tool, WARC-record's anomalies",'output':"",'restriction':"",'description':'''The command line tool shall notify the user of any WARC-record's anomalies, missing required fields or incompatible fields types.'''},

{'id':"149",'groupid':"0",'event':"",'agent':"libwarc",'operation':"provide to a set of classes to",'input':"WARC-records",'output':"classes",'restriction':"",'description':'''Libwarc shall provide a set of classes to enable remote management of WARC-records'''},

{'id':"150",'groupid':"0",'event':"",'agent':"it",'operation':"be possible",'input':"WARCrecords",'output':"",'restriction':"'via http'",'description':'''It shall be possible to perform read operations (read from offset, filters, etc.) on WARCrecords from a remote location via http.'''},

{'id':"151",'groupid':"0",'event':"",'agent':"it",'operation':"not",'input':"WARC-record",'output':"",'restriction':"'not', 'remotely'",'description':'''For security reasons, it shall not be possible to perform write or update operations on a WARC-record remotely'''},

{'id':"152",'groupid':"0",'event':"",'agent':"warc browser",'operation':"not",'input':"warc browser, cdx file, cdx file format",'output':"",'restriction':"'not', 'not'",'description':'''WARC browser shall not support CDX files because the CDX file format is not a standard at this time and is outside of scope.'''},

{'id':"153",'groupid':"0",'event':"",'agent':"warc browser",'operation':"support",'input':"warc browser, archived content, Wayback Machine",'output':"client-side rewriting interface",'restriction':"'by'",'description':'''WARC Browser shall support a client-side rewriting interface by using javascript code to rewrite links being delivered alongside archived content. This is based on the principles implemented in the Wayback Machine.'''},

{'id':"154",'groupid':"0",'event':"",'agent':"interface",'operation':"implement",'input':"live web",'output':"web proxy interface, web browser proxy",'restriction':"'thereby'",'description':'''A web proxy interface shall be implemented that allows the user to set their web browser proxy to the one provided by the interface and thereby ensure all content is delivered from the archive and not from the live web.'''},

{'id':"155",'groupid':"0",'event':"",'agent':"incorporate",'operation':"incorporate",'input':"Apache module, SRS 34-36, Apache",'output':"",'restriction':"'within an Apache module to enable all actions specified in SRS 34-36 to be executed within Apache'",'description':'''Libwarc shall be incorporated within an Apache module to enable all actions specified in SRS 34-36 to be executed within Apache.'''},

{'id':"156",'groupid':"0",'event':"",'agent':"incorporate",'operation':"incorporate",'input':"Lighttp module, SRS 34-36, lighttp",'output':"",'restriction':"'within a Lighttp module to enable all actions specified in SRS 34-36 to be executed within lighttp'",'description':'''Libwarc shall be incorporated within a Lighttp module to enable all actions specified in SRS 34-36 to be executed within lighttp.'''},

{'id':"157",'groupid':"0",'event':"",'agent':"[incorporating libwarc can migrate data in ARC]tool arc2warc",'operation':"migrate",'input':"command line tool, ARC-records, WARC-record format",'output':"arc2warc",'restriction':"",'description':'''A command line tool "arc2warc" incorporating libwarc shall be able to migrate data in ARC-records to WARC-record format.'''},

{'id':"158",'groupid':"0",'event':"",'agent':"default operation[of ]",'operation':"carry",'input':"arc2warc, ARC-record, conversion process",'output':"response, metadata",'restriction':"",'description':'''The default operation of "arc2warc" shall carry out a one-to-one mapping of record fields, by converting each ARC-record to a corresponding "response" WARC-record and "metadata" WARCrecord, which shall include information about the conversion process.'''},

{'id':"159",'groupid':"0",'event':"",'agent':"arc2warc",'operation':"have",'input':"arc2warc, ARC-record, WARC-record",'output':"default operation",'restriction':"'where'",'description':'''"arc2warc" shall have make a default operation in cases where an ARC-record has no corresponding field in the WARC-record.'''},

{'id':"160",'groupid':"0",'event':"",'agent':"it",'operation':"be possible",'input':"arc2warc, named configuration file, ARC-record",'output':"WARC-record",'restriction':"",'description':'''It shall be possible to specify non-default operations of "arc2warc" using a named configuration file, which will describe the desired ARC-record to WARC-record conversion.'''},

{'id':"161",'groupid':"0",'event':"",'agent':"set[of ]",'operation':"perform",'input':"command line tools, HTTrack",'output':"WARC-records",'restriction':"",'description':'''A set of command line tools incorporating libwarc shall perform migration of "HTTrack" archives to WARC-records.'''},

{'id':"162",'groupid':"0",'event':"",'agent':"file format",'operation':"vary",'input':"HTTrack, HTTrack archive file format, migration scripts",'output':"",'restriction':"'therefore'",'description':'''The HTTrack archive file format and link strategy may vary from version to version of HTTrack, therefore it shall be possible to adapt the migration scripts to deal with these changes.'''},

{'id':"163",'groupid':"0",'event':"",'agent':"set[of ]",'operation':"perform",'input':"command line tools, wget",'output':"WARC-records",'restriction':"",'description':'''A set of command line tools incorporating libwarc shall perform migration of "wget" archives to WARC-records.'''},

{'id':"164",'groupid':"0",'event':"",'agent':"set[of ]",'operation':"perform",'input':"command line tools, curl",'output':"WARC-records",'restriction':"",'description':'''A set of command line tools incorporating libwarc shall perform migration of "curl" archives to WARC-records.'''},

{'id':"165",'groupid':"0",'event':"",'agent':"set[of ]",'operation':"enable",'input':"command line tool, API, online documents",'output':"WARC-records",'restriction':"",'description':'''A set of command line tools and an API incorporating libwarc shall enable the collection of online documents, such as html and embedded files, etc., and write them to valid WARC-records.'''},

{'id':"166",'groupid':"0",'event':"",'agent':"line tool",'operation':"not",'input':"command line tools, API",'output':"",'restriction':"'not', 'in SRS'",'description':'''The command line tools and API in SRS 50 will not include any links extraction features.'''},

{'id':"167",'groupid':"0",'event':"",'agent':".",'operation':"implement",'input':"libwarc",'output':"Python scripts",'restriction':"",'description':'''Python scripts shall be implemented incorporating libwarc, and making all of the functionality of libwarc and API available in Python.'''},

{'id':"168",'groupid':"0",'event':"",'agent':".",'operation':"provide",'input':"HTTrack, wget, curl, libwarc",'output':"Extensions",'restriction':"",'description':'''Extensions to "HTTrack", "wget" and "curl" incorporating libwarc shall be provided as patches to recent and specific versions of each tool, to enable users of the tool to access functionality of libwarc'''},

{'id':"169",'groupid':"0",'event':"",'agent':"command",'operation':"make",'input':"HTTrack, wget, curl, libwarc",'output':"Helper documentation",'restriction':"'within the HTTrack'",'description':'''Helper documentation for libwarc functionality shall be made available within the "HTTrack", "wget" and "curl" commands.'''},

{'id':"170",'groupid':"0",'event':"",'agent':"file",'operation':"create",'input':"mime-type database, WARC files",'output':"magic number",'restriction':"'for WARC', 'via the Unix file command'",'description':'''A magic number for WARC shall be created and incorporated in the "file" mime-type database, enabling the simple identification of WARC files via the Unix "file" command'''},

{'id':"171",'groupid':"0",'event':"",'agent':"extract",'operation':"extend",'input':"warc validator tool, Jhove command line, WARC files",'output':"properties",'restriction':"'optionally', 'i.e.', 'well', 'finally'",'description':'''The WARC validator tool specified in SRS 31-32 shall be extended to optionally make use of the Jhove command line API to identify and validate WARC files, i.e. given a specific WARC file, this command shall be able to identify the file as a WARC file, validate the level of compliance with a given standard in terms of well-formedness and validity, and finally to characterise the file by extracting and displaying significant properties contained in the file.'''},

{'id':"172",'groupid':"0",'event':"",'agent':".",'operation':"implement",'input':"Jhove Plugin layer, warc file",'output':"WarcMdoule, WarcHandler plugin modules",'restriction':"",'description':'''WarcMdoule and WarcHandler plugin modules shall be implemented for Jhove Plugin layer to enable identification and validation of WARC files.'''},

{'id':"173",'groupid':"0",'event':"",'agent':".",'operation':"provide",'input':"Jhove deliverables",'output':"test-states",'restriction':"",'description':'''WARC files in various test-states shall be provided that test the Jhove deliverables'''},

{'id':"175",'groupid':"0",'event':"",'agent':"libwarc",'operation':"provide to interfaces to SWIG wrappers to",'input':"",'output':"interfaces to SWIG wrappers, SWIG wrappers, dynamic language bindings",'restriction':"",'description':'''Libwarc shall provide interfaces to SWIG wrappers to allow dynamic language bindings (Python, Ruby, Perl, Lua ...)'''},

{'id':"176",'groupid':"0",'event':"",'agent':".",'operation':"implement",'input':"SWIG wrapper",'output':"Python interface",'restriction':"",'description':'''A Python interface to libwarc shall be implemented using the SWIG wrapper'''},

{'id':"177",'groupid':"0",'event':"",'agent':".",'operation':"implement",'input':"SWIG wrapper, JNI",'output':"Java interface",'restriction':"",'description':'''A Java interface to libwarc shall be implemented using the SWIG wrapper and/or JNI'''},

{'id':"178",'groupid':"0",'event':"",'agent':".",'operation':"implement",'input':"SRS 61",'output':"Java implementation of libwarc",'restriction':"",'description':'''An independent Java implementation of libwarc may be implemented subject to review of deliverables satisfying SRS 61'''},

{'id':"179",'groupid':"0",'event':"",'agent':"libwarc",'operation':"enable",'input':"Libwarc, functionality, iterators, dynamic languages, Java v1.4, metaphors, paradigms",'output':"",'restriction':"'within various dynamic languages and in Java v14 and earlier'",'description':'''Libwarc and the bindings to its functionality shall enable the use of libwarc's iterators described in SRS 16-20 to be used within various dynamic languages and in Java v1.4 and earlier, using metaphors and paradigms familiar to those languages.'''},

{'id':"180",'groupid':"0",'event':"",'agent':"libwarc",'operation':"enable",'input':"Libwarc, functionality, iterators, dynamic languages, Java v1.5, container iterators",'output':"",'restriction':"'within Java v15 and and later'",'description':'''Libwarc and the bindings to its functionality shall enable the use of libwarc's iterators described in SRS 16-20 to be used within Java v1.5 and and later, using Java's new container iterators, such as "for" and "foreach".'''},


]
testF2=[
{'id':"31",'groupid':"0",'event':"",'agent':"system",'operation':"export",'input':"[correct]patient record",'output':"test procedure",'restriction':"",'description':"The system should provide a way to export allergies that have been entered on the wrong patient into the correct patient record. An audit trail must be created in both the incorrect and correct patient records."},

{'id':"205",'groupid':"0",'event':"",'agent':"physician organization instruction",'operation':"have",'input':"[specific][ability]test procedure instruction, physician organization instruction, health organization",'output':"",'restriction':"'within the system or be provided through links to external sources'",'description':"The system should have the ability to provide access to patient-specific test and procedure instructions that can be customized by the physician or health organization these instructions are to be given to the patient.  These instructions may reside within the system or be provided through links to external sources."},
]
CNfunction = [
        {'agent': '评估模型执行功能',
        'description': '当获得仿真试验数据后，评估模型执行功能能够按照评估模型中制定的评估流程，逐步执行计算模型和分析模型过程，最终生成AHP评估模型的评估结果。',
        'event': '当获得仿真试验数据后',
        'groupid': '',
        'id': '0',
        'input': '仿真试验数据, 评估模型中制定的评估流程逐步',
        'operation': '执行',
        'output': 'AHP评估模型的评估结果',
        'restriction': '按照评估模型中制定的评估流程逐步',
        'type': '2'},
        {'agent': '展示方案构建功能',
        'description': '展示方案构建功能能够对展示方案进行保存。',
        'event': '无条件',
        'groupid': '',
        'id': '1',
        'input': '展示方案',
        'operation': '保存',
        'output': '展示方案',
        'restriction': '无约束',
        'type': '2'},
        {'agent': '视图',
        'description': '当展示方案被保存后，展示视图生成功能生成可用于展示的视图。',
        'event': '当展示方案被保存后',
        'groupid': '',
        'id': '2',
        'input': '展示方案',
        'operation': '用于',
        'output': '无输出',
        'restriction': '无约束',
        'type': '2'},
        {'agent': '评估模型执行功能',
        'description': '评估模型执行功能能够根据评估任务的需要，以数据抽取的方式获得所需的仿真试验数据。',
        'event': '无条件',
        'groupid': '',
        'id': '3',
        'input': '评估任务的需要',
        'operation': '获得',
        'output': '数据抽取的方式, 所需的仿真试验数据',
        'restriction': '以数据抽取的方式, 根据评估任务的需要',
        'type': '2'}
]
