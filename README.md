# NAME

mykomap-london-renters-union-site

<br/>

# SYNOPSIS

This is an experiment to configure DCC's [`mykomap`] to display London property licensing. Check out that repository as well.

[1]: https://github.com/DigitalCommons/mykomap


## Running the server

- Start your local server and fire up you local MykoMap instance: <br/>
  `npm run build; npm run server`

Because I'm running it in a docker development container I (marc) have to do:
  `echo "http://$(hostname -I | tr -d ' '):8080"; npm run public-server`


### DCC instructions for map set-up for custom configuration

Update the config file in the src folder:
- Update the baseUri and baseCountryUri
```
const baseUri = "https://dev.lod.coop/coop-name/";
const baseCountryUri = "https://dev.lod.coop/essglobal/2.1/standard/countries-iso/";
```

- Update the mapping in the `rowToObj` transformation object, to match those of your data source, adding your own custom fields where necessary, (uri, name, lat and lang are required)
```
const rowToObj = mkObjTransformer<Row, InitiativeObj>({
  uri: T.prefixed(baseUri).from('Identifier'), // Required field
  name: T.text('').from('Name'), //  Required field
  address: T.text('').from('Address'),
  lat: T.nullable.number(null).from('Latitude'), //  Required field
  lng: T.nullable.number(null).from('Longitude'), // Required field
  manLat: T.nullable.number(null).from('Geocoded Latitude'),
  manLng: T.nullable.number(null).from('Geocoded Longitude'),
  description: T.text('').from('Description'),
  placeId: T.prefixed(basePlaceUri).from("Place ID"),
  economicActivity: T.nullable.text(null).from("Economic Activity"),
});
```

  - Add your custom fields to the field definitions

```
type FieldsDef = Dictionary<PropDef | 'value' >;
const fields: FieldsDef = {
  description: 'value',
  address: 'value',
  placeId: {
    type: "vocab",
    uri: "p:",
  },
  economicActivity: {
    type: "vocab",
    uri: "aci:",
  },
};
```

  - Update the `ConfigData object`, entering the correct values for `namedDataset, htmlTile, filterableFields and searchableFields`. If your map’s vocabs do not conform to `ESSGLOBAL` or have not been confirmed, a local vocabs document can be added to the codebase’s www folder, based on the values of your data sources `filterableFields`. The example below includes both local and remote vocabs.
```
export const config: ConfigData = new ConfigData({
  namedDatasets: ["DatasetName"],
  htmlTitle: "DatasetTitle",
  fields: fields,
  filterableFields: ["economicActivity", "placeId"],
  searchedFields: ["description"],
  languages: ["EN"],
  language: "EN",
  vocabularies: [
    {
      type: "json",
      id: "vocabid",
      label: "VOCABLABEL",
      url: "vocabs.json",
    },
    {
      type: "json",
      id: "essglobal",
      label: "ESSGLOBAL 2.1",
      url: "https://data.datasourceurl.coop/map-owner/vocabs.json",
    },
  ],
  dataSources: [
    {
      id: "data-source",
      label: "DATASOURCE",
      type: "csv",
      url: "https://data.solidarityeconomy.coop/map-owner/standard.csv",
      transform: rowToObj,
    },
  ],
  showDatasetsPanel: false,
  showDirectoryPanel: true,
  customPopup: getPopup, // uncomment if custom popup wanted
  aboutHtml: about, // uncomment if custom about.html wanted
  ...versions,
});
```

  - As with the vocabularies, if you do not have a remote data file, one can be added to the `www/` folder and referenced locally in the `dataSources` object.
- Start your local server and fire up you local MykoMap instance: <br/>
  `npm run build; npm run server`
