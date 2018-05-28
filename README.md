# Ass2

#For each Image
export PROJECT_ID="$(gcloud config get-value project -q)"
docker build -t gcr.io/${PROJECT_ID}/reddit:v1 .
gcloud docker -- push gcr.io/${PROJECT_ID}/server:v1

#This will build and image and push to the google container repo
#we can use these builds in our yaml files later

#run chmod +x Deploy
#run chmod +x Delete

#to start ./Deploy
#to end ./Delete
