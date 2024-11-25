import os
 
#Each Website you crawl is a separate project(folder)

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('creating project' + directory)
        os.makedirs(directory)

create_project_dir('thenewboston')


#Create queue and crawled files (if not create)
def create_data_files(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled,'')

#Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

#Add data onto an existin file 
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data +"\n")

#Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass
    