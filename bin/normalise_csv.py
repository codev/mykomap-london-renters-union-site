#!/usr/bin/env python3
"""
Normalise property licensing CSV data across boroughs.

Creates unified fields and cleans up column names.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


def parse_date(date_str: str) -> str | None:
    """Parse date string and return ISO format (YYYY-MM-DD)."""
    if not date_str or date_str.strip() == '':
        return None

    date_str = date_str.strip()

    # Try ISO format first (YYYY-MM-DD)
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # Try British format (DD/MM/YYYY)
    try:
        dt = datetime.strptime(date_str, '%d/%m/%Y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # Try other common formats
    for fmt in ['%d-%m-%Y', '%Y/%m/%d', '%m/%d/%Y']:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue

    # Return original if unparseable
    return date_str


def coalesce(*values) -> str:
    """Return first non-empty value."""
    for v in values:
        if v and str(v).strip():
            return str(v).strip()
    return ''


# Mapping from original field names to clean names
FIELD_RENAMES = {
    'property_id': 'property_id',
    'borough': 'borough',
    'postcode': 'postcode',
    'address': 'address',
    'license_number': 'license_number',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'bathrooms': 'bathrooms',
    'kitchens': 'kitchens',
    'licence_type': 'licence_type',
    'living_accommodation': 'living_accommodation',
    'sleeping_accommodation': 'sleeping_accommodation',
    'maximum_permitted_households': 'max_households',
    'maximum_permitted_occupants': 'max_occupants',
    'no._of_non_self_contained_flats': 'num_non_self_contained_flats',
    'no._of_self_contained_flats': 'num_self_contained_flats',
    'no._of_storeys': 'num_storeys',
    'property_description': 'property_description',
    'uprn': 'uprn',
    'year_built': 'year_built',
}

# Fields to skip (will be replaced by normalised versions)
SKIP_FIELDS = {
    'licence_end_date',
    'licence_start_date',
    'license_end_date',
    'license_start_date',
    'licence_holder_name',
    'licence_holder_address',
    'licence_reference_number',
    'ten_end_date',
    'ten_start_date',
    'ten_holder_name',
    'ten_holder_address',
    'ten_reference_number',
    'managing_agent_name',
    'managing_agent_address',
}

# Normalised fields to add
NORMALISED_FIELDS = [
    'start_date',
    'end_date',
    'holder_name',
    'holder_address',
    'reference_number',
    'managing_agent',
    'managing_agent_address',
]


def normalise_row(row: dict) -> dict:
    """Create normalised row with clean field names."""
    result = {}

    # Copy and rename standard fields
    for old_name, new_name in FIELD_RENAMES.items():
        if old_name in row:
            result[new_name] = row.get(old_name, '')

    # Normalise start date - prefer ISO format field, fall back to British format
    start_date = parse_date(row.get('license_start_date', ''))
    if not start_date:
        start_date = parse_date(row.get('licence_start_date', ''))
    if not start_date:
        start_date = parse_date(row.get('ten_start_date', ''))
    result['start_date'] = start_date or ''

    # Normalise end date
    end_date = parse_date(row.get('license_end_date', ''))
    if not end_date:
        end_date = parse_date(row.get('licence_end_date', ''))
    if not end_date:
        end_date = parse_date(row.get('ten_end_date', ''))
    result['end_date'] = end_date or ''

    # Normalise holder name - prefer licence_holder, fall back to ten_holder
    result['holder_name'] = coalesce(
        row.get('licence_holder_name', ''),
        row.get('ten_holder_name', '')
    )

    # Normalise holder address
    result['holder_address'] = coalesce(
        row.get('licence_holder_address', ''),
        row.get('ten_holder_address', '')
    )

    # Normalise reference number
    result['reference_number'] = coalesce(
        row.get('licence_reference_number', ''),
        row.get('ten_reference_number', '')
    )

    # Normalise managing agent
    result['managing_agent'] = coalesce(
        row.get('managing_agent_name', '')
    )

    result['managing_agent_address'] = coalesce(
        row.get('managing_agent_address', '')
    )

    return result


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.csv> [output.csv]", file=sys.stderr)
        print("If output.csv is not specified, writes to input_normalised.csv", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent / f"{input_path.stem}_normalised{input_path.suffix}"

    # Build output field order
    output_fields = list(FIELD_RENAMES.values()) + NORMALISED_FIELDS

    with open(input_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=output_fields)
            writer.writeheader()

            count = 0
            for row in reader:
                normalised = normalise_row(row)
                writer.writerow(normalised)
                count += 1

            print(f"Processed {count} rows", file=sys.stderr)
            print(f"Output written to: {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
