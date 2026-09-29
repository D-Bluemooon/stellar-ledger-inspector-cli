import sys
import json
import urllib.request

def analyze_organization_ledger(wallet_id, timeout=10, hide_zero_balances=False, export_json=None):
        target_endpoint = f"https://stellar.org{wallet_id}"
        print(f"[Diagnostic] Fetching metrics from Horizon network node for: {wallet_id}")

    try:
                req = urllib.request.Request(target_endpoint, headers={'User-Agent': 'D-Bluemoon-Bot'})
                with urllib.request.urlopen(req, timeout=timeout) as payload:
                                account_data = json.loads(payload.read().decode())
                                print("\n=== Verified Asset Ledgers ===")
                                balances = account_data.get('balances', [])
                                for asset in balances:
                                                    ticker = asset.get('asset_code', 'XLM') if asset.get('asset_type') != 'native' else 'XLM'
                                                    balance = float(asset.get('balance', 0))

                # Hide zero or low balance assets
                        if hide_zero_balances and balance < 0.01:
                                                continue

                print(f"Asset Pool: {ticker} | Available Balance: {asset.get('balance')}")

            # Export to JSON file
            if export_json:
                                with open(export_json, 'w') as f:
                                                        json.dump(account_data, f, indent=2)
                                                    print(f"\n[Success] Exported ledger data to {export_json}")

except urllib.error.URLError as e:
        if 'timed out' in str(e).lower():
                        print(f"[Error] Request timed out after {timeout} seconds: Horizon node is unresponsive")
else:
            print(f"[Error] Failed to connect to target Horizon endpoint: {e}")
except Exception as network_err:
        print(f"[Error] Unexpected error: {network_err}")

if __name__ == "__main__":
        sample_node = sys.argv if len(sys.argv) > 1 else "GDV7ZVDZCD66UUI7WQZ6G45HVT56Z26J2B7U7Y3T2D36H6Q7P64W3L7Y"
    analyze_organization_ledger(sample_node)
