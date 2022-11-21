#!/bin/sh
echo "insert profile [default=default]"
read PROFILE

echo "input ACCOUNTID"
read ACCOUNTID

echo "region"
read REGION

echo "input CodeCommit's REPOSITORY ARN "
read REPOSITORY

echo "input CodeBuild's Project ARN"
read CODEBUILD

echo "input REFERENCE_TYPE"
read REFERENCE_TYPE

echo "input REFERENCE_NAME"
read REFERENCE_NAME
aws iam --profile=$PROFILE create-role --role-name CodeBuild-Invoke-Role-For-Cloudwatch-Events --assume-role-policy-document file://TrustPolicyForCWE.json

aws iam --profile=$PROFILE put-role-policy --role-name CodeBuild-Invoke-Role-For-Cloudwatch-Events --policy-name CodeBuild-Permissions-Policy-For-CWE --policy-document file://PermissionsPolicyforCWE.json

aws events --profile=$PROFILE put-rule --name "CodeBuildTriggerRule" --event-pattern "{\"source\":[\"aws.codecommit\"],\"detail-type\":[\"CodeCommit Repository State Change\"],\"resources\":[\"$REPOSITORY\"],\"detail\":{\"referenceType\":[\"$REFERENCE_TYPE\"],\"referenceName\":[\"$REFERENCE_NAME\"]}}" --role-arn "arn:aws:iam::$ACCOUNTID:role/CodeBuild-Invoke-Role-For-Cloudwatch-Events"

aws events --profile=$PROFILE put-targets --rule CodeBuildTriggerRule --targets "Id"="1","Arn"="$CODEBUILD","RoleArn"="arn:aws:iam::$ACCOUNTID:role/CodeBuild-Invoke-Role-For-Cloudwatch-Events"