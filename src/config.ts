// Re-export of ConfigData in mykomap/index above seems not to work,
// so import it directly from here:
import { ConfigData } from "mykomap/app/model/config-schema";
import type {
  PropDef
} from "mykomap/app/model/data-services";
import {
  mkObjTransformer,
  Transforms as T,
} from "mykomap/obj-transformer";
import * as versions from "./version.json";

import about from "./about.html";
import { InitiativeObj } from "mykomap/src/map-app/app/model/initiative";

type Row = Record<string, string | null | undefined>;
const baseUri = 'https://hackney.gov.uk/licensing/';

const rowToObj = mkObjTransformer<Row, InitiativeObj>({
  uri: T.prefixed(baseUri).from('property_id'),
  name: T.text('').from('address'),
  address: T.text('').from('address'),
  lat: T.nullable.number(null).from('latitude'),
  lng: T.nullable.number(null).from('longitude'),
  postcode: T.text('').from('postcode'),
});


type Dictionary<T> = Partial<Record<string, T>>;
type FieldsDef = Dictionary<PropDef | 'value'>;
const fields: FieldsDef = {
  address: 'value',
  postcode: 'value',
};


export const config: ConfigData = new ConfigData({
  namedDatasets: ['metastreet'],
  htmlTitle: 'London Property Licensing',
  defaultLatLng: [51.545, -0.055],
  fields: fields,
  filterableFields: [],
  searchedFields: [
    'address',
    'postcode',
  ],
  languages: ['EN'],
  language: 'EN',
  vocabularies: [],
  dataSources: [
    {
      id: 'metastreet',
      label: 'MetaStreet Data',
      type: 'csv',
      url: 'AllMetaStreet_slim.csv',
      transform: rowToObj,
    },
  ],
  showDatasetsPanel: false,
  showDirectoryPanel: true,
  aboutHtml: about,
  ...versions,
});
