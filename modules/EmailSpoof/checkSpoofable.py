#!/usr/bin/env python

import dns.resolver
import re
import sys
from colorama import Fore, init, Style

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

def getSPF(resolver, domain):
	spfRegex = re.compile("^\"(v=spf1).*\"$")
	try:
		answer = resolver.resolve(domain, 'txt')
		for item in answer.response.answer:
			for line in item.items:
				if spfRegex.match(line.to_text()):
					return str(line)
	except dns.resolver.NoAnswer:
		return False

def getDMARC(resolver, domain):
	spfRegex = re.compile("^\"(v=DMARC).*\"$")
	try:
		answer = resolver.resolve("_dmarc." + domain, 'txt')
		for item in answer.response.answer:
			for line in item.items:
				if spfRegex.match(line.to_text()):
					return str(line)
	except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
		return False

def main():
	try:
		domain = sys.argv[1]
		resolver = dns.resolver.Resolver()
		spfRecord = getSPF(resolver, domain)
		spoofable = False
		if spfRecord:
			spfRecord = spfRecord.strip('"')
			print("[" + Fore.BLUE + "X" + Style.RESET_ALL + "] SPF record found: ")
			print(spfRecord)
			if "~all" not in spfRecord and "-all" not in spfRecord:
				print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] " + domain + " does not contain \"-all\" or \"~all\" in the SPF record.\n")
				spoofable = True
		else:
			print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] SPF record not found for " + domain + "\n")
			spoofable = True
		dmarcRecord = getDMARC(resolver, domain)
		dmarcTagRegex = r";\s*p=([^;]*)\s*;"
		dmarcTagMatch = None
		if dmarcRecord:
			dmarcRecord = dmarcRecord.strip('"')
			dmarcTagMatch = re.search(dmarcTagRegex, dmarcRecord)
		dmarcTag = None 
		if dmarcTagMatch:
			dmarcTag = dmarcTagMatch.group(1)
		if dmarcRecord:
			print("[" + Fore.BLUE + "X" + Style.RESET_ALL + "] DMARC record found: ")
			print(dmarcRecord)
			if not dmarcTagMatch:
				print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] " + domain + " does not have a policy set in the DMARC record.\n")
				spoofable = True
			elif dmarcTag == "none":
				print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] " + domain + " has policy set to \"none\" in the DMARC record.\n")
				spoofable = True
		else:
			print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] DMARC record not found for " + domain + "\n")
			spoofable = True
		if spoofable:
			print("\n" + Fore.GREEN + domain + " is spoofable.")
		else:
			print("\n" + Fore.RED + domain + " is NOT spoofable.")
	except dns.resolver.LifetimeTimeout:
		print("\n\033[93m DNS EXCEPTION: DNS LOOKUP TIME OUT")
		print("-----------------------------------")
	except Exception:
		print("\n\033[93m PLEASE GIVE DOMAIN NAME AS INPUT")
		print("--------------------------------")

if __name__== "__main__":
	init(autoreset=True)
	main()
	