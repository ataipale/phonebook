#!/usr/bin/env python

'''
Requirements:
    pip install pymongo
    brew install mongodb

    run the command 'sudo mongod' before running this program to initiate connection to mongodb
'''

import sys
import pymongo

def create(phonebook_name):
    '''create database to hold phonebook entries'''
    if phonebook_name not in phonebook_db.collection_names():
        getattr(phonebook_db, phonebook_name)
    else:
        print "That phonebook already exists"

def lookup(name, phonebook_name):
    '''return the number of a person in the phonebook'''
    if phonebook_name in phonebook_db.collection_names():
        collection_pointer = getattr(phonebook_db, phonebook_name)
        p = [i for i in collection_pointer.find({'name' : name})]
        if p:
            print p.pop().get('phone')
        else:
            "%s does not exist" %name
    else:
        print "%s does not exist" %phonebook_name

def add(name, number, phonebook_name):

    '''add person to db'''
    
    if phonebook_name in phonebook_db.collection_names():
        collection_pointer = getattr(phonebook_db, phonebook_name)
        p = [i for i in collection_pointer.find({'name' : name})]
        if p: 
            print "Duplicate entry, %s not changed" %name
        else: 
            collection_pointer.insert({'name':name, 'phone':number})
    else:
        print "No phonebook called %s" % phonebook_name

def change(name, number, phonebook_name):

    '''change pre-existing entry'''

    if phonebook_name in phonebook_db.collection_names():
        collection_pointer = getattr(phonebook_db, phonebook_name)
        if not collection_pointer.update({'name':name}, {'name':name, 'phone':number}, upsert = False):
            print "%s does not exist in %s" %(name, phonebook_name)
    else:
        print "No phonebook called %s" % phonebook_name

def remove(name, phonebook_name):

    '''remove person from db'''
    
    if phonebook_name in phonebook_db.collection_names():
        collection_pointer = getattr(phonebook_db, phonebook_name)
        if not collection_pointer.remove({'name':name}):
            print "%s does not exist in %s" %(name, phonebook_name)
    else:
        print "No phonebook called %s" % phonebook_name

def reverse_lookup(number, phonebook_name):

    '''return person matching phone number'''
    
    if phonebook_name in phonebook_db.collection_names():
        collection_pointer = getattr(phonebook_db, phonebook_name)
        p = [i for i in collection_pointer.find({'phone' : number})]
        if p: #need to pop to get dict from list
            print p.pop().get('name')
        else:
            "%s does not exist" %name
    else:
        print "%s does not exist" %phonebook_name

if __name__ == '__main__':

    client = pymongo.MongoClient() #pointer at server
    phonebook_db = client.phonebook_db # pointer at phonebook database

    args = sys.argv[:]
    args.pop(0)
    command = args.pop(0)

    if command == 'create':
        create(*args)
    elif command == 'lookup':
        lookup(*args)
    elif command == 'add':
        add(*args)
    elif command == 'change':
        change(*args)
    elif command == 'remove':
        remove(*args)
    elif command == 'reverse-lookup':
        reverse_lookup(*args)
    else:
        print "Not a command"
