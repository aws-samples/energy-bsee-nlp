## Well Analytics with Amazon Comprehend

TODO: Fill this README out!

Be sure to:

* Change the title in this README
* Edit your repository description on GitHub

### Directions:
1) In your AWS account, execute the CloudFormation template 'CFN-Pipeline.yml'. Provide an email that will be later used as login for accessing the Kibana Dashboard
2) Once the stack is finished deploying, upload the contents of the 'Code' folder, along with the 'Buildspec.yml' and 'WellAnalytics-CFN.zip' files to that S3 folder.
3) Navigate to Code Pipeline to monitor the status of the workflow. After a few seconds, the 'Source' should change from a 'Failed' state to a 'Succeeded' state, indicating that the pipeline has recognized the recent changes (new files) that were uploaded to the S3 bucket.
4) Once the pipeline reaches it's 'Deployment' stage, a new CloudFormation template will be automatically executed in the account. This template will take 10-15 minutes to fully deploy. Once it has finished, navigate to the 'Step-Functions' service.
5) Under Step Functions, there will be 'State Machine'. Open it, and click 'Start Execution'. Leave the input parameters as are, and continue with the 'Start Execution' option. This will trigger a series of Lambda functions responsible for pulling in the necessary BSEE Well Analytics source data and training the Comprehend Entity Recognizer.
6) The state machine will take about an hour to finish executing and training. Once that is complete, the data should soon be ready, it will send the free form text from the data to Amazon Comprehend. You can view the progress of these jobs in the console under the Amazon Comprehend Service. 
7) Once all analysis jobs are complete, the data will soon be ready to view on Kibana. Navigate back to Cloudformation, under the 'output' tab of the 'WellAnalytics-CFN' stack, you will see a URL that redirects to a Kibana login page. Use the email given in step 1 along with the password that was sent to the respective inbox to login. You will be prompted to change your password.
8) You must now create a index. 
## License

This library is licensed under the MIT-0 License. See the LICENSE file.

