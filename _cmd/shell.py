# -*- coding:utf8 -*-

import subprocess

import dsf

def get_output_from_command(cmd, cwd=None):
	with dsf.core.fs.pushd(cwd):
		# make sure there is a record of what we are doing
		dsf.dslog.log_command_start(cmd)

		# run the command
		p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		# get the output
		output = p1.communicate()

		# put a copy of the output in the log file
		dsf.dslog.log_command_output(output)
		dsf.dslog.log_command_result(p1.returncode)

		# all done
		return output

def run(cmd, cwd=None):
	with dsf.core.fs.pushd(cwd):
		cmd_to_run = _command_to_string(cmd)

		# make sure there is a record of what we are doing
		dsf.dslog.log_command_start(cmd_to_run)

		# run the command
		retval = subprocess.call(cmd_to_run, stdout=dsf.core.log.LOG_STDOUT, stderr=dsf.core.log.LOG_STDERR)

		# make sure there's a record of the command's exit code
		dsf.dslog.log_command_result(retval)

		# let the caller raise the exception - it makes things much
		# easier to understand when looking at the logs
		return retval

def run_with_passthru(cmd, cwd=None):
	with dsf.core.fs.pushd(cwd):
		# make sure there is a record of what we are doing
		dsf.dslog.log_command_start(cmd)

		# run the command
		retval = subprocess.call(cmd)

		# make sure there's a record of the command's exit code
		dsf.dslog.log_command_result(retval)

		# let the caller raise the exception - it makes things much
		# easier to understand when looking at the logs
		return retval

def _command_to_string(cmd):
	# as Python's subprocess module is utterly fucked when using shell=True,
	# we have to emulate the correct behaviour ourselves

	cmd_string="'"
	for param in cmd:
		cmd_string = cmd_string + param + " "
	cmd_string = cmd_string + "'"

	retval=["/bin/bash", "-c", cmd_string]
	return retval
