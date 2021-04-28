import os, sys
import freesound as fs
import json



def downloadSoundsFreesound(search_type=None, queryText = "", target=None, id=None, tags=None, duration=None, API_Key = "chnqxOZ35DAhmdHPAQaOs0bOXFbUNVc5Os0MimA6", outputDir = "", topNResults = 5, featureExt = '.json', descriptors = ['lowlevel.mfcc.mean'], flt_desc = None, filter = None):
  """
  This function downloads sounds and their descriptors from freesound using the queryText and the 
  tag specified in the input. Additionally, you can also specify the duration range to filter sounds 
  based on duration.
  
  Inputs:
        (Input parameters marked with a * are optional)
        queryText (string): query text for the sounds (eg. "violin", "trumpet", "cello", "bassoon" etc.)
        tag* (string): tag to be used for filtering the searched sounds. (eg. "multisample",  
                       "single-note" etc.)
        duration* (tuple): min and the max duration (seconds) of the sound to filter, eg. (0.2,15)
        API_Key (string): your api key, which you can obtain from : www.freesound.org/apiv2/apply/
        outputDir (string): path to the directory where you want to store the sounds and their 
                            descriptors
        topNResults (integer): number of results(sounds) that you want to download 
        featureExt (string): file extension for storing sound descriptors
  output:
        This function downloads sounds and descriptors, and then stores them in outputDir. In 
        outputDir it creates a directory of the same name as that of the queryText. In this 
        directory outputDir/queryText it creates a directory for every sound with the name 
        of the directory as the sound id. Additionally, this function also dumps a text file 
        containing sound-ids and freesound links for all the downloaded sounds in the outputDir. 
        NOTE: If the directory outputDir/queryText exists, it deletes the existing contents 
        and stores only the sounds from the current query. 
  """ 
  
  # Checking for the compulsory input parameters
  # if queryText == "":
  #   print("\n")
  #   print("Provide a query text to search for sounds")
  #   return -1
    
  if API_Key == "":
    print("\n")
    print("You need a valid freesound API key to be able to download sounds.")
    print("Please apply for one here: www.freesound.org/apiv2/apply/")
    print("\n")
    return -1
    
  if outputDir == "" or not os.path.exists(outputDir):
    print("\n")
    print("Please provide a valid output directory. This will be the root directory for storing your descriptors")
    return -1    
  
  # Setting up the Freesound client and the authentication key
  fsClnt = fs.FreesoundClient()
  fsClnt.set_token(API_Key,"token")  
  
  # Creating a duration and tag filter string that the Freesound API understands
  if duration and type(duration) == tuple:
    flt_dur = " duration:[" + str(duration[0])+ " TO " +str(duration[1]) + "]"
  else:
    flt_dur = ""
 
  if tags and type(tags) == list:
    flt_tag = ""
    for tag in tags:
      flt_tag += " tag:"+tag
  else:
    flt_tag = ""

  if id and type(id) == int:
    flt_id = "id:"+str(id)

  filter = flt_id + flt_dur + flt_tag
  if filter == "":
    filter = None
  

  # Querying Freesound
  page_size = 30

  if search_type == "text":
    search_result = fsClnt.text_search(query=queryText, filter = filter, sort="rating_desc", fields="id,name,previews,username,url,analysis", descriptors=','.join(descriptors), page_size=page_size, normalized=1)
  if search_type =="content":
    search_result = fsClnt.content_based_search(target=target, descriptors_filter=flt_desc)
  if search_type =="combined":
    search_result = fsClnt.content_based_search(queryText=queryText, target=target, filter=flt_tag + flt_dur)
  if search_type == "id":
    search_result = fsClnt.text_search(query=queryText, filter = filter, sort="rating_desc", fields="id,name,previews,username,url,analysis", descriptors=','.join(descriptors), page_size=page_size, normalized=1)

  queryDir = os.path.join(outputDir, queryText)    # Directory for each label
  if os.path.exists(queryDir):             # If the directory exists, it deletes it and starts fresh
      os.system("rm -r " + queryDir)
  os.mkdir(queryDir)

  pageNo = 1
  sndCnt = 0
  indCnt = 0
  totalSnds = min(search_result.count,200)   # System quits after trying to download after 200 times
  
  # Creating directories to store output and downloading sounds and their descriptors
  soundList = []
  features = {}
  while(1):
    if indCnt >= totalSnds:
      print("Not able to download required number of sound features. Either there are not enough search results on freesound for your search query and filtering constraints or something is wrong with this script.")
      break
    sound = search_result[indCnt - ((pageNo - 1) * page_size)]
    print("Downloading descriptors for sound with id: %s"%str(sound.id))
    # outDir1 = os.path.join(outputDir, queryText, str(sound.id))
    # if os.path.exists(outDir1):
    #   os.system("rm -r " + outDir1)
    # os.system("mkdir " + outDir1)
    # if os.path.exists(outDir2):
    #   os.system("rm -r " + outDir2)
    # os.system("mkdir " + outDir2)
    
    # mp3Path = os.path.join(outDir2,  str(sound.previews.preview_lq_mp3.split("/")[-1]))
    # ftrPath = mp3Path.replace('.mp3', featureExt)
    # globalPath = os.path.join(queryDir, "urls" + featureExt)
    
    try:
      # fs.FSRequest.retrieve(sound.previews.preview_lq_mp3, fsClnt, mp3Path)                   # downloads and stores the mp3 file
      # Initialize a dictionary to store descriptors
      # if sndCnt == 0: 
        # features = {}
        
      # Obtaining all the descriptors
      for desc in descriptors:
        if desc not in features:
          features[desc] = []
        features[desc].append(eval("sound.analysis." + desc))
        # features[desc] = eval("sound.analysis." + desc)

      # Once we have all the descriptors, store them in a json file
      # json.dump(features, open(ftrPath, 'w'))
      # json.dump(features, open(globalPath, 'a'), indent=4)      
      sndCnt += 1
      soundList.append([str(sound.id), sound.url])

    except:
      pass
      # if os.path.exists(outDir1):
      #   os.system("rm -r " + outDir1)
    
    indCnt += 1
    
    if indCnt%page_size==0:
      search_result = search_result.next_page()
      pageNo+=1
      
    if sndCnt>=topNResults:
      break

  # Dump the list of files and Freesound links
  if features:
    # json.dump(features, open(globalPath, 'w'), indent=4)
    fid = open(os.path.join(queryDir, queryText+'_SoundList.txt'), 'w')
    for elem in soundList:
      fid.write('\t'.join(elem)+'\n')
    fid.close()
    # return features, soundList
    return features
  else:
    return None

  
