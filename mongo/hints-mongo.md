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
