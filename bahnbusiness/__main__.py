#!/usr/bin/env python

import argparse

import bahnbusiness


def main():
  parser = argparse.ArgumentParser(
    description='Download all available tickets and save them into the current directory',
  )

  db = bahnbusiness.BahnApi()
  db.login()

  for journey in db.get_journeys():
    filename = '{}.pdf'.format(journey.id)

    print("Found ticket {} for {} ({}), saving to {}".format(
      journey.id,
      journey.name_booking,
      journey.route,
      filename
    ))

    ticket = db.download_ticket(journey)

    with open(filename, 'wb') as f:
      f.write(ticket)



if __name__ == '__main__':
  main()
