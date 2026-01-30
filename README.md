# NAME

mykomap-site-example

<br/>

# SYNOPSIS

This is a demonstration/pilot project showing how to use the [`mykomap`][1] package.

[1]: https://github.com/DigitalCommons/mykomap

For details of how to do that, see the `mykomap` project's own
documentation. This is merely a supplementary example, which you can
use to base new projects on.

<br/>

# New Map Creation

The following documents the creation a new MykoMap instance, and assumes the existence of the correct Linux / WSL environment.


## Setting up your new map repo

- Clone the mykomap-site-example to your local directory and create a new folder for your MykoMap instance <br/>
```
git clone --depth 1 git@github.com:DigitalCommons/mykomap-site-example.git my-new-mykomap
```
- Navigate to mykomap-site-example directory <br/>
```
cd mykomap-site-example
```
- Remove old Git history and configerations <br/>
```
rm -rf .git
```
- Start fresh with a clean Git repo <br/>
```
git init
```
- Add and commit files to the new repo<br/>
```
git add -A
git commit -m "initial commit"
```
- Optional step - rename local master branch to main <br/>
```
git branch -m master main
```
- Create new remote repository \* <br/>
\*This step can be carried out earlier in the process, if desired
<br/>

- Set the remote origin to your new repo and push to main
```
git remote add origin git@github.com:DigitalCommons/my-new-mykomap
git push --set-upstream origin/main
```
- Create a development branch <br />
```
git checkout –b development
```


## Configuring your local map

Create a `config` folder in the root directory of your new MykoMap instance : <br />
```
  mkdir config
```
or if you have VS Code open, just create a new folder in the root directory.


### Map set-up for initial testing
- Point the `dataSources url` within `src/config.ts` to `example.csv`

```
dataSources: [
    {
      id: 'data-exaple-update-me',
      label: 'UPDATE ME',
      type: 'csv',
      url: 'example.csv',
      transform: rowToObj,
    },
],
```

- Start your local server and fire up you local MykoMap instance: <br/>
  `npm run build; npm run server`


### Map set-up for custom configuration

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
