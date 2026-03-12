"""
#### FLAME DELIVERY HELPER ####


Goal is to take the fewest number of supervisor approved timelines and break them out into the various deliverables required when shipping a project.

This will be done with a tool that takes a delivery matrix (spreasheet formatted as csv) + a selection of hero timelines and attempts to break the fewest number of timelines into the largest number of deliverables on the list as possible.

At the end of the process, it will place all created timelines into one new reel on the desktop titled "ship" output a CSV indicating each file identified from original matrix and whether a file was successfully made, and the resulting name of that file.

- (human) QC final picture/graphics on hero timeline for each spot, make sure to include placeholder slate/2-pop and any black frames at end and in/out for picture to picture (unslated) exports
- (human) QC mixes to be used
- (human) Ensure files are named in a way that will be friendly to the tool, and that the captions and graphics tracks are named appropriately in each timeline
- (human) Ensure both stereo and web mixes are present in timeline and tracks are labelled correctly
- (human) Ensure the desktop has a reel called "shipping_slates" and it is populated with correctly named slates (isci_filename formatting)
- (human) Select all timelines to be used in export, and run command
----------------------
First though, we need to learn how to make slates. To start with, we need to name the files to correspond to what information is on the slate.
So let's assume that we have our sequences for delivery all made, and we just need to rename them. The name will be a concatenation of information on the delivery csv.

- First proof of concept that you can add a slate, 2-pop, and necessary gap to a selected sequence with hardcoded slate name.
----------------------
Now we can try it procedurally, with one resolution, 16x9
- First generate deliverable names from the csv and return as a list of dictionaries, keeping other slate/delivery information attched to the name. 
- Then make that more flame accessible by placing blank sequences named by following the items in list in a reel called "ship_names"
- Now we need to copy and paste those to our timelines (a bit of manual labor here, maybe create copy_name, and paste_name tools?)
- Now, we should be able to select the files, select the csv again, and the sequeneces will be slated correctly w/ slate, 2-pop, and gap.
----------------------
- #### IGNORE THIS LINE, ASSUME FOR NOW SLATES ARE PROVIDED IN DESKTOP REEL CALLED "slates"#### Prompts user for client name, agency name, project name, delivery date (will gather mix levels, duration, as needed from timeline)
- Prompts for delivery matrix to uploaded as .csv 
- Creates list of dict "files_to_ship" to track each identified deliverable from .csv
    - isci - AD ID code
    - filename - Filename as formatted on matrix
    - shipped_filename - isci_filename (where illegal characters are removed and spaces replaced with underscores)
    - parent - Name of which of the selected timelines this file will derive from 
    - captioned - Whether selected file is a titled/captioned version or not
    - titled - Whether selected file is a titled version or not
    - generic - Whether selected file is a generic version or not
    - mix - Whether selected file will have a "web" or a "broadcast" mix
    - delivered - Default to "no" (will toggle to "yes" if file export succesful)
    - filepath - Default to "" (will be replaced with export path if file export succesful)
----------------------
- For item in files_to_ship 
    - Find source timeline in selection
    - Duplicate the source timeline
    - Rename new timeline to shipped_filename 
    - Target captions/graphics tracks as neccessary
    - Target stereo/web mix as necessary
    - Find cooresponding slate by isci in slate reels and place into timeline
    - Export timeline using correct template, placing into timestamped postings folder
    - If export succesful, update in export_spreadsheet whether the file was shipped or not and what path it was exported to 
- Export export_spreadsheet to pipeline folder when finished, first showing alphabetized list of shipped files, then showing alphabetized list not-shipped files


Questions: 
- Can Flame target tracks by their names?
- Can Flame use the gathered info to make slates? 
    - Can Flame pythonically target individual text nodes in a batch per file? (Maybe there is a template for a node called "CLIENT", "DATE", etc.)
    - Can Flame pythonically populate text field fo text node
    - Can Flame put batch output somewhere useful (either on timeline or as exported png from a standalone batch).
- What mixdown in template will be needed if two stereo tracks are present (but one is always muted)?

##################################################################

First steps...Find delivery matrix csv and extract list of filenames
FIND CSV MATRIX 

"""