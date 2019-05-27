import argparse
from datetime import datetime
import json
import os
import xml.etree.ElementTree as ET


def yb2gps(opts):
    with open(os.path.expanduser(opts.setup), 'r') as f:
        setup = json.load(f)

    with open(os.path.expanduser(opts.positions), 'r') as f:
        records = json.load(f)

    root = ET.Element("gpx")

    for record in records:
        trk = ET.SubElement(root, "trk")
        name = ET.SubElement(trk, "name")
        boat_id = record['id']
        team = setup['teams'][boat_id - 1]
        name.text = '{}/{}'.format(team['name'].encode('ascii', 'ignore'), team['model'].encode('ascii', 'ignore'))

        trkseg = ET.SubElement(trk, "trkseg")

        moments = record['moments']
        for moment in moments:
            t = moment['at']
            if 'finishedAt' in team and (team['start'] <= t <= team['finishedAt']):
                trkpt = ET.SubElement(trkseg, "trkpt")
                trkpt.set('lat', str(moment['lat']))
                trkpt.set('lon', str(moment['lon']))
                time = ET.SubElement(trkpt, "time")
                time.text = '<time>{}</time>'.format(datetime.utcfromtimestamp(t)
                                                     .strftime('%Y-%m-%dT%H:%M:%SZ'))
    tree = ET.ElementTree(root)
    tree.write(os.path.expanduser(opts.gpx))
    print '{} GPX file was created'.format(opts.gpx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--positions", help="Positions JSON file ", required=True)
    parser.add_argument("--setup", help="Race Setup JSON file ", required=True)
    parser.add_argument("--gpx", help="Output GPX file", required=True)
    args = parser.parse_args()

    yb2gps(args)
