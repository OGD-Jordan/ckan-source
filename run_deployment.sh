#!/bin/bash

file="deployment_commands.txt"

while IFS= read -r command;  do
	echo "Executing: $command"
	eval "$command"
done < "$file"
