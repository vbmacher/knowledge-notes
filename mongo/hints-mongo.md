# Show progress of indexing

db.currentOp(
    {
      $or: [
        { op: "command", "query.createIndexes": { $exists: true } },
        { op: "none", ns: /\.system\.indexes\b/ }
      ]
    }
)

# Show progress of mapreduce

db.currentOp({"query": /mapreduce/})

# Mongo: selectors

BSONDocument("$nin" -> (.., .., ...))  ==> "not in"

# Show chunks per shards

var db = db.getSiblingDB("config");
db.chunks.find({'_id': /funnel/})
    .sort( { min : 1 } )
    .forEach(function(chunk){
        print( "\n" + tojson( chunk.min ) + " -->> " + tojson( chunk.max ) +
        " id : " + chunk._id +  " on : " + chunk.shard + " " + tojson( chunk.lastmod ) + " " + ( chunk.jumbo ? "jumbo " : "" ));
    }
);


# Find dupes

db.getCollection('funnel_aggregates').aggregate([
  {$match: { 'date': ISODate('2017-01-01') }},
  {$group: { _id: {'domain': '$domain', 'category': '$category', 'brand': '$brand', 'product': '$product', 'date':'$date'}, 'ids': { $addToSet: '_id' } }},
  {$match: { ids: { $gt: 1 }}}
])

# Find unique combinations of things which equal or unequal

db.getCollection('cross_aggregates').aggregate([
  {$match: {'date': {$gte: ISODate("2018-09-01")}}},
  {$project: {
      'd': {$cond: {
               if: { $eq: [ "", "$domain" ] },
               then: "",
               else: "X"
           }},
      'cd': {$cond: {
               if: { $eq: [ "", "$crossDomain" ] },
               then: "",
               else: {
                   $cond: {
                       if: { $eq: ["$domain", "$crossDomain"] },
                       then: "X",
                       else: "Y"
                       }
               }
           }},
      'b': {$cond: {
               if: { $eq: [ "", "$brand" ] },
               then: "",
               else: "A"
           }},
      'cb': {$cond: {
               if: { $eq: [ "", "$crossBrand" ] },
               then: "",
               else: {
                   $cond: {
                       if: { $eq: ["$brand", "$crossBrand"] },
                       then: "A",
                       else: "B"
                       }
               }
           }}
  }},
  {'$group': { '_id': {'d': '$d', 'cd': '$cd', 'b': '$b', 'cb': '$cb'}}}
], {'allowDiskUse': true}) 

