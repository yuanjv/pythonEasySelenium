#a selenium auto script for https://github.com/cmdr2/stable-diffusion-ui
#v2.4.24
import time
import os
from easySelenium import EasySelenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json


class StableDiffusionWeb(EasySelenium):
    def __init__(self, prompt:str, nPrompt:str, seed:int, model:str, vae:str, sampler:str, size:list, guidance:float, step:int, amount:int, wait:int, link:str="localhost:9000", imgDir:str=os.path.join(os.path.dirname(__file__),"sdImg"), headless:bool=True, fixFace:bool=True, resX4:bool=True):
        super().__init__(link, headless)

        #settings@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #prompt
        self.idRewrite("prompt",prompt)

        # negative prompt
        if nPrompt!=None:
            self.eClick('id','negative_prompt_handle')
            self.idRewrite("negative_prompt",nPrompt)
        
        #setting manu
        self.eClick("id","editor-settings")

        #seed
        if seed!=None:
            self.eClick("id","random_seed")
            self.idRewrite("seed",seed)
        
        #model
        self.idSelectDropdown("stable_diffusion_model",model)

        #vae
        if vae==None:
            vae="None"
        self.idSelectDropdown("vae_model",vae)

        #sampler
        self.idSelectDropdown("sampler",sampler)

        #size
        try:
            self.idSelectDropdown("width",str(size[0]))
        except:
            self.idSelectDropdown("width",str(size[0])+" (*)")
        time.sleep(3)
        try:
            self.idSelectDropdown("height",str(size[1]))
        except:
            self.idSelectDropdown("height",str(size[1])+" (*)")
        
        #guidance
        defaultG=7.5
        if guidance!=None:
            guidanceLevel=self.driver.find_element("id","guidance_scale_slider")
            while(guidance>defaultG):
                guidanceLevel.send_keys(Keys.ARROW_RIGHT)
                guidance-=0.1
            while(guidance<defaultG):
                guidanceLevel.send_keys(Keys.ARROW_LEFT)
                guidance+=0.1
        
        #step
        if step!=None:
            self.idRewrite("num_inference_steps",step)

        #fix face
        self.sendToTheBottom()
        if fixFace:
           self.eClickUltra("id","use_face_correction")
        
        #resX4
        if resX4:
            self.eClickUltra("id","use_upscale")

           
        
        #settings DONE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        #make sure the folder exits
        os.system("mkdir "+imgDir)

        #make current time as new image dir
        fileDir=os.path.join(imgDir,os.popen('date +%Y-%m-%d@%H:%M:%S').read().strip('\n'))
        os.system("mkdir "+fileDir)
        
        #wait
        time.sleep(int(wait)*60)

        imgInfoNotExist=True

        for i in range(amount):
            #start
            self.eClick("id","makeImage")



            #wait for the img
            time.sleep(5)
            self.waitUntilDisappear("id","stopImage",10)

            #save the pic
            imgInfo=self.driver.find_element("class name","taskConfig").text
            imgSeed=imgInfo.split(", ")[0].replace("Seed: ","")
            
            self.saveFromSrc(["class name","imgContainer","css selector","img"],os.path.join(fileDir,imgSeed+".jpg"))

            #write info into img dir
            if imgInfoNotExist:
                settings=imgInfo.split(", Negative Prompt:")[0].split(", ")
                dic={"Prompt":prompt,"Negative Prompt":nPrompt,"Size":size,"VAE":vae}
                for setting in settings:
                    setting=setting.split(": ")
                    dic[setting[0]]=setting[1]
                js=json.dumps(dic,indent=4)
                print(js)
                os.system(f"echo '{js}' > {os.path.join(fileDir,'info.json')}")
                imgInfoNotExist=False
        
            #reset window
            self.sendToTheTop()
            self.keyDown(Keys.SHIFT)
            self.eClickUltra("id","clear-all-previews")
            self.keyUp(Keys.SHIFT)
        
        #end 
        time.sleep(10)
        self.close()
