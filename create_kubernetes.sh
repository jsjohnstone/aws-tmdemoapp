#!/usr/bin/env bash
# Command to create cloudformation-controlled kubernetes cluster
eksctl create cluster --name tm-app --nodegroup-name standard-workers --node-type t2.micro --nodes 2 --nodes-min 1 --nodes-max 3 --node-ami auto