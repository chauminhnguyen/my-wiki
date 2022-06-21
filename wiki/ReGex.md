<details>
<summary><b>Tranfer a file via SSH. </b></summary>
  
  **Type below command at local computer.**
  - *From local computer to ssh server:*
    ```sh
    scp -P port_number path/to/file_name username@server-ip:/path/to/destiny
    ```
  - *From ssh server to local computer:*
    ```sh
    scp -P port_number username@server-ip:/path/to/file_name path/to/destiny 
    ```
  If you want transfer a folder add `-r` prefix

</details>

<details>
<summary><b>Limit cpu usage of a running process.</b></summary>
  
  ```sh
  cpulimit -l cpu_usage_limitation(%) -p PID_num_of_process
  cpulimit -l 120 -p 3198
  ```
  To check PID_num of a running prosess use `htop`.
  
</details>

<details>
<summary><b>Check Server's Tensorboard-Logs on Local machine.</b></summary>
  
  ```sh
  tensorboard --logdir=logs_dir --host localhost --port 8888
  ```
  
</details>
