import json
from argparse import ArgumentParser
from pathlib import Path
from pprint import pprint

import requests
from dotenv import load_dotenv
from logzero import logger
from td_connect import TDAuth

if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument('symbol', help='Symbol to get data for.')
    parser.add_argument('--type', '-t', choices=['fundamental', 'chain', 'quote'], default='fundamental', help='Type of data to get.')
    parser.add_argument('--env_t', '-e', choices=['gcs','local'], default='gcs', help='Environmental variable for configuration file.')
    parser.add_argument('--env_file', '-f', help='Path to .env file.')
    parser.add_argument('--save_path', '-p', help='Path to file where data should be saved.')
    
    args = parser.parse_args()
    
    if args.env_file:
        load_dotenv(args.env_file)
    else:
        load_dotenv()
    
    if args.env_t == 'gcs':
        auth = TDAuth.from_gcs_env()
    elif args.env_t == 'local':
        auth = TDAuth.from_env()
        
    endpoint_params = {
        'fundamental': {
            'endpoint': 'https://api.tdameritrade.com/v1/instruments',
            'params': {
                'symbol': args.symbol,
                'projection': 'fundamental'
            } 
        },
        'chain': {
            'endpoint': 'https://api.tdameritrade.com/v1/marketdata/chains',
            'params': {
                'symbol': args.symbol,
                # The number of strikes to return above and below the at-the-money price.
                'strikeCount': 100,
                'includeQuotes': True,
            }   
        },
        'quote': {
            'endpoint': f'https://api.tdameritrade.com/v1/marketdata/{args.symbol}/quotes',
            'params': {}, 
        }
    }
    cfg = endpoint_params[args.type]
    cfg['params']['apikey'] = auth.client_id
    
    resp = requests.get(cfg['endpoint'], params=cfg['params'], headers=auth.auth_header)
    logger.info(f"[{resp.status_code}] {cfg['endpoint']}")
    
    data = resp.json()
    
    pprint(data)
    
    if args.save_path:
        Path(args.save_path).write_text(json.dumps(data, indent=4))
