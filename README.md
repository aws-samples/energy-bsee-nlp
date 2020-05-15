## Analyze drilling reports using natural language processing with Amazon Comprehend


### Directions:
1) In your AWS account, execute the CloudFormation template 'CFN-Pipeline.yml'. Provide an email that will be later used as login for accessing the Kibana Dashboard
2) Once the stack is finished deploying, upload the contents of the 'Code' folder, along with the 'Buildspec.yml' and 'WellAnalytics-CFN.zip' files to that S3 folder.
3) Navigate to Code Pipeline to monitor the status of the workflow. After a few seconds, the 'Source' should change from a 'Failed' state to a 'Succeeded' state, indicating that the pipeline has recognized the recent changes (new files) that were uploaded to the S3 bucket.
4) Once the pipeline reaches it's 'Deployment' stage, a new CloudFormation template will be automatically executed in the account. This template will take 10-15 minutes to fully deploy. Once it has finished, navigate to the 'Step-Functions' service.
5) Under Step Functions, there will be 'State Machine'. Open it, and click 'Start Execution'. Leave the input parameters as are, and continue with the 'Start Execution' option. This will trigger a series of Lambda functions responsible for pulling in the necessary BSEE Well Analytics source data and training the Comprehend Entity Recognizer.
6) The state machine will take about an hour to finish executing and training. Once that is complete, the data should soon be ready, it will send the free form text from the data to Amazon Comprehend. You can view the progress of these jobs in the console under the Amazon Comprehend Service. 
7) Once all analysis jobs are complete, the data will soon be ready to view on Kibana. Navigate back to Cloudformation, under the 'output' tab of the 'WellAnalytics-CFN' stack, you will see a URL that redirects to a Kibana login page. Use the email given in step 1 along with the password that was sent to the respective inbox to login. You will be prompted to change your password.
8) You must now create an index pattern. Navigate to your Elasticsearch cluster's public domain, and find the gear option in the navigation bar on the left hand side of the screen.
9) Run through the directions for setting up an index pattern (if the data has begun loading in, you should see an 'events' index). Select "EVENT_DATE" as the time filter field name, and create the index.
10) You will now be able to see the items in your dashboard (may need to adjust the time range). Create custom visualizations and see what valuable insights you can gain from the data!

#### Closing Notes
a) If you have chosen the 'Test' option when originally deploying the Cloud Formation template, you will only have a couple of data points in visible in the Elasticsearch cluster. For a full data set, navigate into the QuickDataLoad directory locally (one you cloned from GitHub). Run the following commands, making sure to substitute the parameters in '< >' with their respective values.
#### pip install Elasticsearch
#### pip install requests_aws4auth
#### python TrainingData.py <Elasticsearch endpoint> <region>

b) To clean up, delete all the contents of the S3 bucket <accountId>-bsee-well-analytics. Then, delete the cloudFormation template (WellAnalytics-CFN). Wait for this to finish deleting. Once complete, clear the contents of the S3 bucket <accountId>-bsee-sourcecode (note this bucket has versioning, so you may need to click show all versions before deleting everything). Finally, delete the original cloud formation template you launched at the beginning of this walkthrough

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

