# VIMEO

### Upload screen 

###### Review link

```html
    <input type="text" class="sc-fQejPQ fBezwT" readonly="" value="https://vimeo.com/warc/review/393645443/2700ee5b9b" aria-invalid="false" format="neutral" id="copyField">
```

###### Title

`<input type="text" name="name" class="setting_input" value="131458v01">`

### Videos screen

###### Tick box

`<span class="sc-itybZL cvTPVK"><div class="sc-jVODtj juLDPW"></div></span>`

###### Titles & Review
   
`<a target="_blank" href="/393645443/settings" title="131459v01">`

### Showcase screen 
- https://vimeo.com/manage/showcases/6815373/info

I wonder if this would be different for every showcase...

```html
        <div role="row" class="sc-LzNtR dKgIcl" style="z-index: 0; background-color: rgb(255, 255, 255); transform: translate3d(0px, 6256px, 0px); cursor: default; box-shadow: rgba(0, 0, 0, 0.2) 0px 1px 4px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px;">
        <div class="sc-LzNtV dKOusV">
        <div class="sc-LzNvT dVijzZ">
        <svg viewBox="0 0 20 20" class="sc-LzNvP dUAxjp">
        <path d="M16 8h-1V5A5 5 0 0 0 5 5v3H4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zM7 5a3 3 0 0 1 6 0v3H7z" fill="#1a2e3b">
        </path>
        </svg>
        <a href="/manage/393645178/general" target="_blank" class="sc-fzXfMD ccGNay sc-LzNwr eftCcU">
        	<span format="primary" class="sc-fzXfME dgbrhe">131463v01</span></a></div><div class="sc-LzNws efBYHd"></div></div>

        		<a href="/manage/393645178/general" target="_blank" class="sc-fzXfMD ccGNay sc-LzNwr eftCcU">

        			<span format="primary" class="sc-fzXfME dgbrhe">131463v01</span></a>
```

---
# NEWCMS

## Batch Actions page

- http://newcms.warc.com/content/batch-actions

This has potential to mark content live, much more accurate than ticking all the boxes individually.

- ID Range (smallest and largest value in list / csv column)
- Source dropdown menu
- View button

Click through >>>

- Tick boxes
- ID matching
- Make live button

## Edit page

- http://newcms.warc.com/content/edit

This would need a for loop and a csv accounting for multiple videos (v01, v02, etc.), and an additional column stating 'Creative' or 'Campaign' like in the production video spreadsheet:

| Video     | Title                   | Link      | Type     |
|-----------|-------------------------|-----------|----------|
| 131076v01 | Coca-Cola: Share a Coke | 33i487z12 | Campaign |
| 131076v02 | Coca-Cola: Share a Coke | 3d94870q2 | Creative |
| 131076v03 | Coca-Cola: Share a Coke | 33p4a7012 | Creative |
| 131098v01 | McDonald's: Shake'N'Dip | 3p3u6k5de | Campaign |

Rather than having a 'Title' column to populate the title input in the below html, this could just be taken directly from the article metadata.

Currently I'm using an extra column for 'ID' in front of 'Video', but this seems like needless duplication, as I could just do `row['Video'][6:]`, to remove the v0 number when used to enter the article.

###### ID input

It would be more efficient to stay within the same ID and not keep saving and going into the same ID multiple times. 

I'm not sure how I would achieve this if going `for row in csv_file:` unless I make a header for each video, its link, its code, its type for all 3 potential videos. This would require a fair amount of configuring and more time, whereas ideally I want to be able to create the csv by exporting or pasting directly from the Videos tab in the main EDIT.xlsx file - which is in the vertical format above, as it originates from running `os.listdir()` or `ls -Filter File | Select-Object -BaseName / Name` on the directory.

```html
    <input class="form-text-input" data-val="true" data-val-number="The field WARC ID must be a number." id="LegacyId" name="LegacyId" type="text" value="">
```

###### Submit / Edit button

`<input type="submit" value="Edit">`

This cannot be done directly in the url sadly. But *can* be done with `send_keys(Keys.RETURN)` rather than clicking.

- `http://newcms.warc.com/content/edit/{ID number}`
- `http://newcms.warc.com/content/edit/casestudy/dfde202c-1c90-4be1-8948-6bb753375b5c`

---

#### Metadata tab

Default set to dropdown automatically, but this is the hover tag:

```html
    <a class="accordion-toggle collapsed" data-toggle="collapse" href="#collapseMetadata" role="button" aria-expanded="false" aria-controls="collapseMetadata">Metadata</a>
```

The dropped down section menu:

```html
    <div id="content-metadata-section" class="form-group">
        <div class="form-body">
            <input data-val="true" data-val-required="The ContentTemplateType field is required." id="ContentTemplateType" name="ContentTemplateType" type="hidden" value="CaseStudy" aria-describedby="ContentTemplateType-error" class="valid" aria-invalid="false">
```

###### Title input

```html
    <input class="form-text-input valid" data-val="true" data-val-required="The Title field is required." id="Title" name="Title" type="text" value="Al Rajhi Bank: The Woman Behind the Veil" aria-describedby="Title-error" aria-invalid="false">
```

This could be used for the video renaming instead of a column in the csv as mentioned above.

###### Additional information

```html
    <input class="form-text-input valid" id="AdditionalInformation" name="AdditionalInformation" type="text" value="Entrant, Effective Use of Tech, 2019" aria-invalid="false">
```

As a bonus, this could automate adding fields in front of the Category, Year format.

**Shortlist announcements:**

-  Shortlisted

**Winners announcements:**

-  Entrants
-  Winners
    - Grand Prix
    - Gold
    - Silver
    - Bronze
    - Special Awards

Winners have to strip out the existing 'Shortlisted,' which could possibly be done with a `value.replace('Shortlisted', medal)` from the value field. 

Hopefully can get there by targeting in Selenium the same way as CSS:

- `<div id="content-metadata-section" class="form-group">`
- `<div class="form-body">`
- target through class: `<input class="form-text-input valid"`
- target through ID: `id="AdditionalInformation"`
- then value: `value="Entrant, Effective Use of Tech, 2019"`

This could be from the same csv I create for PR and News currently, which I also use to create Winners landing pages. This would save a huge amount of time, especially for entrants.

Ideally, as with the ticket raised for bulk adding videos - as we do with abstracts, metadata, images, etc. - we should be able to bulk edit metadata to change these. I've raised this before, but no idea if it's even in the pipeline.

---

#### Summary tab

###### Generate bullets button

I think accordion has to be toggled from collapsed (default):

```html
    <a class="accordion-toggle collapsed" data-toggle="collapse" href="#collapseSummary" role="button" aria-expanded="false" aria-controls="collapseSummary">Summary</a>
```

To expanded:

```html
    <a class="accordion-toggle" data-toggle="collapse" href="#collapseSummary" role="button" aria-expanded="true" aria-controls="collapseSummary">Summary</a>
```

Before I can click generate bullets:

```html
    <button id="GenerateBullets" type="button" class="box-links mb-md-std-space" onclick="onGenerateBulletedSummaryClicked('')">Generate Bullets</button>
```

But perhaps this can be actioned, rather than clicked.

    <span class="std-link-style" onclick="onExpandAllClicked();">Expand all</span>

Articles don't do this automatically, so this takes forever to go through and do. Much easier to proof the abstract files first, use my cleaner script etc. and then generate them all after batch uploading.

```python
def generate_bullets(self):
        bot = self.bot
        bot.find_element_by_link_text('Summary').click()
        logger.info("clicked [Summary] (Expand)")
        bot.find_element_by_id('GenerateBullets').click()
        logger.info("clicked [Generate Bullets]")
```

---

#### Videos tab

Might be different for campaign vs creative, also don't know what this looks like for the blank panel before you add a video.

```html
        <a class="accordion-toggle" data-toggle="collapse" href="#collapseVideos" role="button" aria-expanded="true" aria-controls="collapseVideos">Videos</a>
        <div class="form-page video-sub-container" data-video="11499">
                <div class="content-ordering-arrows">
                    <button type="button" class="button-up anchor-style" onclick="onMoveVideoUpClicked(event)"><img src="/images-site/actions/chevron-up.svg" alt="Up"></button>
                    <button type="button" class="button-down anchor-style" onclick="onMoveVideoDownClicked(event)"><img src="/images-site/actions/chevron-down.svg" alt="Down"></button>
                </div>
```

###### Review link ID label and input

```html
<div class="row mt-medium-space mt-xl-half-space">
    <label class="col-3 col-sm-2" for="VideoViewModels_0__VideoLink">ID</label>
    <div class="col-7 col-sm-9 col-md-2 required">
        <input class="form-text-input valid" data-val="true" data-val-required="Enter the video ID" data-video-link="" id="VideoViewModels_0__VideoLink" name="VideoViewModels[0].VideoLink" type="text" value="363774128" aria-describedby="VideoViewModels_0__VideoLink-error" aria-invalid="false">
        <span class="field-validation-valid" data-valmsg-for="VideoViewModels[0].VideoLink" data-valmsg-replace="true"></span>
        <input data-val="true" data-val-number="The field VideoId must be a number." data-val-required="The VideoId field is required." data-video-id="" id="VideoViewModels_0__VideoId" name="VideoViewModels[0].VideoId" type="hidden" value="11499" aria-describedby="VideoViewModels_0__VideoId-error" class="valid" aria-invalid="false">
    </div>
    <label class="col-3 col-sm-2 col-md-1 offset-md-2 offset-xl-1" for="VideoViewModels_0__VideoType">Type</label>
```

Campaign Video is the default selected option. Creative would be the other, hence the need for the 'Type' column in the csv file.

```html
                <div class="col-7 col-sm-9 col-md-3 required">
                    <select class="form-text-input" data-video-type="" id="VideoViewModels_0__VideoType" name="VideoViewModels[0].VideoType"><option selected="selected" value="Campaign Video">Campaign video</option>
    <option value="Creative">Creative</option>
    <option value="Event">Event</option>
    <option value="Interview">Interview</option>
    <option value="Overview">Overview</option>
    <option value="Webinar">Webinar</option>
    </select>
                </div>
            </div>
```

###### Video title label and input

This line indicates the current title: `value="Al Rajhi Bank: The Woman Behind the Veil"`

```html
                <div class="row mt-md-medium-space">
                    <label class="col-sm-2" for="VideoViewModels_0__VideoTitle">Title</label>
                    <div class="col-10 col-sm-9 col-md-8 required">
                        <input class="form-text-input valid" data-val="true" data-val-required="Enter the video Title" data-video-title="" id="VideoViewModels_0__VideoTitle" name="VideoViewModels[0].VideoTitle" type="text" value="Al Rajhi Bank: The Woman Behind the Veil" aria-describedby="VideoViewModels_0__VideoTitle-error" aria-invalid="false">
                        <span class="field-validation-valid" data-valmsg-for="VideoViewModels[0].VideoTitle" data-valmsg-replace="true"></span>
                    </div>
                </div>
```

###### Caption label and input

Pretty sure this isn't required.

```html
                <div class="row mt-md-medium-space">
                    <label class="col-sm-2" for="VideoViewModels_0__VideoCaption">Caption</label>
                    <div class="col-10 col-sm-9 col-md-8">
                        <input class="form-text-input valid" data-video-caption="" id="VideoViewModels_0__VideoCaption" name="VideoViewModels[0].VideoCaption" type="text" value="" aria-invalid="false">
                    </div>
                </div>
```

###### Featured label and tick box

I think this automatically sets to featured when saved, despite being required.

```html
                <div class="row mt-md-medium-space">
                    <div class="offset-sm-2 col">
                        <input data-val="true" data-val-required="The Featured? field is required." id="VideoViewModels_0__VideoFeatured" name="VideoViewModels[0].VideoFeatured" type="checkbox" value="true" aria-describedby="VideoViewModels[0].VideoFeatured-error" class="valid" aria-invalid="false"><input name="VideoViewModels[0].VideoFeatured" type="hidden" value="false" aria-describedby="VideoViewModels[0].VideoFeatured-error" class="valid" aria-invalid="false"><label for="VideoViewModels_0__VideoFeatured" title="Featured?"><span></span>Featured?</label>
                    </div>
                </div>
```

###### Remove video button

```html
                <div class="row">
                    <div class="col-10 col-sm-11 col-md-10 form-buttons">
                        <input type="button" class="box-links warning valid" value="Remove" onclick="onRemoveVideoClicked(event, '11499')" aria-invalid="false">
                    </div>
                </div>
            </div>
```

###### Add a new video

```html
            <input type="button" class="box-links mt-4 valid" value="Add another" id="add-video-button" onclick="onAddVideoClicked()" aria-invalid="false">
            <div id="video-template" style="display: none" data-template="">
```

###### Blank video template 

Expands when button clicked: `onclick="onMoveVideoDownClicked(event)"`.

```html       
        <div class="video-container">
            <div class="form-page video-sub-container" data-video="0">
                <div class="content-ordering-arrows">
                    <button type="button" class="button-up anchor-style" onclick="onMoveVideoUpClicked(event)"><img src="/images-site/actions/chevron-up.svg" alt="Up"></button>
                    <button type="button" class="button-down anchor-style" onclick="onMoveVideoDownClicked(event)"><img src="/images-site/actions/chevron-down.svg" alt="Down"></button>
                </div>
                <div class="row mt-medium-space mt-xl-half-space">
                    <label class="col-3 col-sm-2" for="AddedVideo_VideoLink">ID</label>
                    <div class="col-7 col-sm-9 col-md-2 required">
                        <input class="form-text-input" data-val="true" data-val-required="Enter the video ID" data-video-link="" id="AddedVideo_VideoLink" name="AddedVideo.VideoLink" type="text" value="">
                        <span class="field-validation-valid" data-valmsg-for="AddedVideo.VideoLink" data-valmsg-replace="true"></span>
                        <input data-val="true" data-val-number="The field VideoId must be a number." data-val-required="The VideoId field is required." data-video-id="" id="AddedVideo_VideoId" name="AddedVideo.VideoId" type="hidden" value="0">
                    </div>
                    <label class="col-3 col-sm-2 col-md-1 offset-md-2 offset-xl-1" for="AddedVideo_VideoType">Type</label>
                    <div class="col-7 col-sm-9 col-md-3 required">
                        <select class="form-text-input" data-video-type="" id="AddedVideo_VideoType" name="AddedVideo.VideoType"><option value="Campaign Video">Campaign video</option>
        <option value="Creative">Creative</option>
        <option value="Event">Event</option>
        <option value="Interview">Interview</option>
        <option value="Overview">Overview</option>
        <option value="Webinar">Webinar</option>
        </select>
                    </div>
                </div>
                <div class="row mt-md-medium-space">
                    <label class="col-sm-2" for="AddedVideo_VideoTitle">Title</label>
                    <div class="col-10 col-sm-9 col-md-8 required">
                        <input class="form-text-input" data-val="true" data-val-required="Enter the video Title" data-video-title="" id="AddedVideo_VideoTitle" name="AddedVideo.VideoTitle" type="text" value="">
                        <span class="field-validation-valid" data-valmsg-for="AddedVideo.VideoTitle" data-valmsg-replace="true"></span>
                    </div>
                </div>
                <div class="row mt-md-medium-space">
                    <label class="col-sm-2" for="AddedVideo_VideoCaption">Caption</label>
                    <div class="col-10 col-sm-9 col-md-8">
                        <input class="form-text-input" data-video-caption="" id="AddedVideo_VideoCaption" name="AddedVideo.VideoCaption" type="text" value="">
                    </div>
                </div>
                <div class="row mt-md-medium-space">
                    <div class="offset-sm-2 col">
                        <input data-val="true" data-val-required="The Featured? field is required." id="AddedVideo_VideoFeatured" name="AddedVideo.VideoFeatured" type="checkbox" value="true"><input name="AddedVideo.VideoFeatured" type="hidden" value="false"><label for="AddedVideo_VideoFeatured" title="Featured?"><span></span>Featured?</label>
                    </div>
                </div>
                <div class="row">
                    <div class="col-10 col-sm-11 col-md-10 form-buttons">
                        <input type="button" class="box-links warning" value="Remove" onclick="onRemoveVideoClicked(event, '0')">
                    </div>
                </div>
            </div>
        </div>
        </div>
```

Only needed if within the same session, each time the ID is entered, it reverts back to `AddedVideo0` etc.

```python
def add_video(self, vnum, vlink, vtype): # , vtitle
    bot = self.bot

    def scroll():
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        logger.info('scroll')

    def add_video():
        bot.find_element_by_id('add-video-button').click()
        logger.info('clicked [Add]')
        
    article_title = bot.find_element_by_id('Title').get_attribute('value')
    logger.info('article title - ' + article_title)
    scroll()
    time.sleep(1)

    if 'v01' in vnum:
        link = bot.find_element_by_id('AddedVideo0_VideoLink').send_keys(vlink)
        title = bot.find_element_by_id('AddedVideo0_VideoTitle').send_keys(article_title)

        if vtype == 'Creative':
            vid_type = bot.find_element_by_id('AddedVideo0_VideoType').click()
            vid_type = bot.find_element_by_xpath('//option[@value="Creative"]').click()
        else:
            pass
        # bot.find_element_by_id("AddedVideo0_VideoFeatured").click()

    if 'v02' in vnum:
        link = bot.find_element_by_id('AddedVideo1_VideoLink').send_keys(vlink)
        title = bot.find_element_by_id('AddedVideo1_VideoTitle').send_keys(article_title)
        
        if vtype == 'Creative':
            vid_type = bot.find_element_by_id('AddedVideo1_VideoType').click()
            vid_type = bot.find_element_by_xpath('//option[@value="Creative"]').click()
        else:
            pass
            
        # bot.find_element_by_id("AddedVideo1_VideoFeatured").click()

    if 'v03' in vnum:
        link = bot.find_element_by_id('AddedVideo2_VideoLink').send_keys(vlink)
        title = bot.find_element_by_id('AddedVideo2_VideoTitle').send_keys(article_title)
        
        if vtype == 'Creative':
            vid_type = bot.find_element_by_id('AddedVideo2_VideoType').click()
            vid_type = bot.find_element_by_xpath('//option[@value="Creative"]').click()
        else:
            pass
            
        # bot.find_element_by_id("AddedVideo2_VideoFeatured").click()
```

Problem with this was that the dropdown menu would only be changed for the first video each time. Required more exact xpath targeting to fix:

```python
def add_video(self, vnum, vlink, vtype): # , vtitle
        bot = self.bot

        def scroll():
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            logger.info('scroll')

        def add_video():
            bot.find_element_by_id('add-video-button').click()
            logger.info('clicked [Add]')
            
        article_title = bot.find_element_by_id('Title').get_attribute('value')
        logger.info('article title - ' + article_title)
        scroll()
        time.sleep(1)

        if 'v01' in vnum:
            bot.find_element_by_link_text('Videos').click() 
            logger.info('clicked [Videos] (Expand)')
            scroll()
            time.sleep(1)
            add_video() # changes to Add another, but id stays the same
            link = bot.find_element_by_id('AddedVideo0_VideoLink').send_keys(vlink)
            logger.info('link - ' + vlink)
            title = bot.find_element_by_id('AddedVideo0_VideoTitle').send_keys(article_title)
            logger.info('vid title - ' + article_title)
            
            if 'Creative' in vtype:
                vid_type = bot.find_element_by_id('AddedVideo0_VideoType').click()
                logger.info('clicked Type')
                time.sleep(1)
                select_type = bot.find_element_by_xpath(
                    '//select[@id="AddedVideo0_VideoType"]//option[@value="Creative"]').click()
                logger.info('selected Creative')
                time.sleep(1)
            else:
                pass

        if 'v02' in vnum:
            scroll()
            time.sleep(1)
            add_video()
            link = bot.find_element_by_id('AddedVideo1_VideoLink').send_keys(vlink)
            logger.info('link - ' + vlink)
            title = bot.find_element_by_id('AddedVideo1_VideoTitle').send_keys(article_title)
            logger.info('vid title - ' + article_title)

            if 'Creative' in vtype:
                vid_type = bot.find_element_by_id('AddedVideo1_VideoType').click()
                logger.info('clicked Type')
                time.sleep(1)
                select_type = bot.find_element_by_xpath(
                    '//select[@id="AddedVideo1_VideoType"]//option[@value="Creative"]').click()
                logger.info('selected Creative')
                time.sleep(1)
            else:
                pass

        if 'v03' in vnum:
            scroll()
            time.sleep(1)
            add_video()
            link = bot.find_element_by_id('AddedVideo2_VideoLink').send_keys(vlink)
            logger.info('link - ' + vlink)
            title = bot.find_element_by_id('AddedVideo2_VideoTitle').send_keys(article_title)
            logger.info('vid title - ' + article_title)

            if 'Creative' in vtype:
                vid_type = bot.find_element_by_id('AddedVideo2_VideoType').click()
                logger.info('clicked Type') # log
                time.sleep(1)
                select_type = bot.find_element_by_xpath(
                    '//select[@id="AddedVideo2_VideoType"]//option[@value="Creative"]').click()
                logger.info('selected Creative') # log
            else:
                pass
```

###### Save changes

`<span onclick="onSaveClicked()">Save </span>`

Solved with:
    
```python
def save_changes(self):
    bot = self.bot
    bot.find_element_by_xpath('//span[@onclick="onSaveClicked()"]').click()
    logger.info('Saved changes')
```

