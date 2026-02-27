I just installed a proxmox cluster with 2 nodes and Proxmox VE 9. 
Configure the proxmox cluster and prepare it to deploy a k8s cluster with multiple nodes. Make sure you chose libraries and modules that are compatible with Proxmox VE 9.
You have root access to proxmox nodes. It's meant only for initial deployment phase. Create service account or new users if needed for the long run. Initial credentials and secrets will be revoked/rotated by the User once the deployment is ready.
The k8s cluster should optimize all resource that is has on the proxmox cluster. 
The k8s should be a HA cluster, with an ingress controller and a hello world application. 
The ingress cluster should be accesible from the local network