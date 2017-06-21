


db.getCollection('channel_mappings').find({}).forEach(function(rec){
        db.profile_to_tg.find({}).forEach(function(tg_rec){
            var region = rec.region
            var channel = rec.channel_name
            var nccs, age, gender
            tg = tg_rec.tg.split('/')
//             print (tg)
            nccs = tg[0].split("")
            age = tg[1]
            gender = tg[2]
            if (gender == "MF") gender = ["Male", "Female"]
            else if(gender == "F") gender = ["Female"]
            else gender = ["Male"]
//             print([region, channel, age, nccs, gender])

           r = db.rationale.findOne({region: region, channel: channel, age: age, gender: gender, nccs: nccs})
            if (!r) print([region, channel, age, nccs.join(""), gender])
//            
        })
})
