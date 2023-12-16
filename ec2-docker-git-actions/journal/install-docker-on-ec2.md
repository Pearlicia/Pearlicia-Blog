# Install Docker on Ubuntu EC2 Instance

Here are the steps to install docker into your EC2 Instance

1. You can use local SSH or use Putty if you are using Windows to connect your Ubuntu EC2 Instace. 
You can also directly use the web console by clicking into your EC2 instance name and choosing `connect`.

2. Update and Upgrade packages
Ensure your system is up-to-date with the latest packages by running the update and upgrade commands.
```bash
sudo apt update && sudo apt upgrade -y
```
This ensures your system is equipped with the latest security patches and improvements.

3. Add Docker’s package repository
Prepare your system to fetch Docker's repository key and add the official repository.
- Install necessary tools and dependencies for secure package retrieval.
```bash
sudo apt install ca-certificates curl gnupg lsb-release
```
- Download Docker's GPG key and store it securely.
```bash
sudo mkdir -p /etc/apt/keyrings
```
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
- Add Docker's official repository for Ubuntu.
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
- Refresh your package lists after adding the Docker repository.
```bash
sudo apt update
```

4. Install Docker Community Education
Install Docker Community Edition along with essential tools.
- Install Docker and its components to enable containerization.
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- Verify the successful installation of Docker.
```bash
docker -v
```
- Check the status of the Docker service.
```bash
systemctl status docker --no-pager -l
```

5. Add your Ubuntu user to the Docker Group
Grant Docker privileges to your Ubuntu user.
- Include your user in the Docker group to execute Docker commands without sudo.
```bash
sudo usermod -aG docker $USER
```
- Check if your user has been added to the Docker group successfully.
```bash
id $USER
```

6. Reload the Shell Session
Activate the changes by reloading the shell session.

- Refresh your user's group memberships to apply Docker group changes.
```bash
newgrp docker
```

7. Test Docker by installing an Image
Ensure Docker is functioning correctly by running a test image, like Hello-world.
```bash
docker run hello-world
```