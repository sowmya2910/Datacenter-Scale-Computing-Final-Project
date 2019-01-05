Integrating Spark on a Kubernetes Cluster and running a Spark Job on Kubernetes 

The 2 main steps to be followed are:
1. Creating a Kubernetes cluster on AWS (EKS Cluster).
2. Installation of Spark 2.3 on local system and running Spark Jobs on the EKS cluster. 


The following steps are taken to setup a Kubernetes cluster on AWS (EKS).

1. Created a role called amgoEKS with the AmazonEKSClusterPolicy, AmazonEKSServicePolicy

2. Created security groups

3. Created cluster VPC

4. Set up the aws-iam-authenticator for Amazon EKS in the local setup
	 a. curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/darwin/amd64/aws-iam-authenticator
	 b. chmod +x ./aws-iam-authenticator
	 c. echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
	 d. export PATH=$HOME/go/bin:$PATH && echo 'export PATH=$HOME/go/bin:$PATH' >> ~/.bashrc

5. Set up kubectl in the local setup 
	 a. curl -o kubectl https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/kubectl
     b. chmod +x ./kubectl
	 c. mkdir $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH

6. Set up the AWS CLI
	 a. pip install awscli --upgrade --user
     b. Run aws configure
		i. 	Enter AWS ACCESS ID
		ii. Enter AWS ACCESS SECRET KEY
        iii.Enter Region

7. Creating EKS Cluster:
	 a. Enter cluster name
     b. Enter the role created before
     c. Enter the VPC created
     d. Choose the subnets 
     e. Choose the security groups
     f. Wait till the clusters are created

8. After successfully creating the EKS, the next step would be to update kubectl.
	 a. aws eks update-kubeconfig --name cluster_name
 	 b. Test the configuration by entering "kubectl get svc"

9. Launch the EKS Worker Nodes
	 a. The EKS Control Plane had been set up till now.
	 b. Wait for the cluster to become active
	 c. Create stack
	 d. Choose Template and specify an amazon S3 template URL
	 e. Pasted the https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2018-11-07/amazon-eks-nodegroup.yaml 
	 f. In the next step, specify the following details. 
		 i.   Stack Name
         ii.  Cluster Name
         iii. Choose the Security Groups
         iv.  NodeGroupName
	     v.   NodeAutoScalingGroupMinSize
         vi.  NodeAutoScalingGroupMaxSize
         vii. NodeInstanceType
         viii.NodeImageId
         ix.  Keyname
         x.   Bootstrap Arguments
     g. Record the NodeInstanceRole after creating the worker nodes


10. Enable the worker nodes to join the cluster	
	 a. Download the configuration map aws-auth-cm.yaml
     b. Replace <ARN of instance role (not instance profile)> snippet with the NodeInstanceRole recorded in the previous step
     c. kubectl apply -f aws-auth-cm.yaml
     d. Verify the status of the nodes by running the command "kubectl get nodes --watch"


The following steps are followed for the  Installation of Spark 2.3 on local system and running Spark Jobs on the EKS cluster

1. Download the Spark 2.3 binary files which contains the binaries, examples and jars.

2. Set the environment variables. For example, if the Spark 2.3 files are stored in /home/amith/spark2.3. 
   Set SPARK_HOME environment variable to /home/amith/spark2.3. Set JAVA_HOME to /usr/lib/jvm/java-8-openjdk-amd64/jre

3. Run kubectl cluster-info to obtain the Kubernetes Cluster Master URL. (For Eg. k8s://https://023A5D0723D5C7A7880DF9494BD6E32D.yl4.us-west-2.eks.amazonaws.com)

4. Since the triggering of spark jobs needs to be done from the local system, the following command must be executed for the local machine
   to be given access to the Kubernetes cluster.
	
	kubectl create clusterrolebinding cluster-system-anonymous --clusterrole=cluster-admin --user=system:anonymous

5. Using this kubernetes master URL and the spark-submit binary, we could execute a command to run the spark job 
   in the kubernetes cluster.
		
			spark-submit \
				--master k8s://https://023A5D0723D5C7A7880DF9494BD6E32D.yl4.us-west-2.eks.amazonaws.com  \
			    --deploy-mode cluster \
			    --name spark-pi  \
			    --class org.apache.spark.examples.SparkPi \
	            --conf spark.executor.instances=3 \
                --conf spark.kubernetes.authenticate.driver.serviceAcountName=arn:aws:eks:us-west-2:948306487609:cluster/TaxiCluster01 \
                --conf spark.kubernetes.container.image=kubespark/spark-init:v2.2.0-kubernetes-0.5.0 
                --conf spark.kubernetes.namespace=kube-system \ 
                local:///home/amith/Downloads/spark-2.3.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.3.0.jar

6. The above command would run a spark job on the kubernetes cluster represented by the URL.


