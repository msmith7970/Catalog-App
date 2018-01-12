from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista",
             email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')

session.add(User1)
session.commit()


# Category for Fishing
category1 = Category(user_id=1, name="Fishing")

session.add(category1)
session.commit()

print 'category name = ' + category1.name



Item1 = Item(user_id=1,
             name="Zebco Pole",
             description="Crappie Pole. Light weight for some Live Action.  Great companion in the Spring time when calling in sick to work.",
             category_name=category1.name)

session.add(Item1)
session.commit()

print 'category_name = ' + Item1.category_name
print 'category name round 2 = ' + category1.name
print 'item 1 user id = ' + str(Item1.user_id)
print 'item 1 name = ' + Item1.name
print 'item 1 description = ' + Item1.description
print 'item 1 category = ' + Item1.category_name


#print 'Category1 Name=' + category1.name
Item2 = Item(user_id=1,
             name="Zebco Reel",
             description="Zebro 33 Baitcast Reel.  Tangle Free but not guranteed to be tangle free when fishing in the tree tops.  Look out outlaw Crappie Charlie here we go.",
             category_name=category1.name)
              # price="$29.97",
              # or category=category1)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Crappie Grub",
             description="2 inch artifical grubs with scent attraction.  Simulates live bait with a curly tail",
             category_name=category1.name)
            # price="$2.97",
            # or category=category1)

session.add(Item3)
session.commit()

Item4 = Item(user_id=1,
             name="Minnow Bucket",
             description="Styrofoam minnow bucket.  Don't get me wrong artifical bait will work but don't be caught on the lake when the only thing they are hitting is LIVE BAIT.",
             category_name=category1.name)
            # price="$14.97",
            # or category=category1)

session.add(Item4)
session.commit()


# Category for Hunting
category2 = Category(user_id=1,
                     name="Hunting")

session.add(category2)
session.commit()

print 'Category2 Name=' + category2.name

Item1 = Item(user_id=1,
             name="Scent-Lock Bowhunting Jacket",
             description="Carbon Allow technology, Microflease liner, All-Season versatility. Colors vary by location.",
             category_name=category2.name)
            # price="$74.97",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Camo Hunting Boots",
             description="200 gram 3M Thinsulate, Lightweight Construction.",
             category_name=category2.name)
            # price="$79.97",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Dove Vest",
             description="Mesh panels for breathability, Large bloodproof game bag, Accessory pockets, zip front.",
             category_name=category2.name)
            # price="$79.97",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="12 Guage Shells",
             description="Federal Game-Shok, Heavy Field. 12 ga 1/8 oz.  25 Shells per box.",
             category_name=category2.name)
            # price="$79.97",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Boating
category3 = Category(user_id=1,
                    name="Boating")

session.add(category3)
session.commit()

print 'Category3 Name=' + category3.name

Item1 = Item(user_id=1,
             name="Tracker Boat",
             description="17 foot Bass Pro Tracker Boat.  All Aluminum construcion. With 40 HP Mercury.  Foot controlled trolling motor and Depth finder.  Comes with heavy guage steel trailer.",
             category_name=category3.name)
            # price="$7799.99",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Life Jacket",
             description="Personal flotation device when operating a boat.  You'll be glad you got this with you when the game warden pulls.",
             category_name=category3.name)
             # price="$7799.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Portable Gas Tank",
             description="All plastic construcion with 6 ft hose. Life time warranty.",
             category_name=category3.name)
            # price="$49.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="Anchor",
             description="40 lb led Anchor.  A must need item for keeping that perfect spot.",
             category_name=category3.name)
            # price="$39.99",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Archery
category4 = Category(user_id=1,
                    name="Archery")

session.add(category4)
session.commit()

print 'Category4 Name=' + category4.name

Item1 = Item(user_id=1,
             name="Compund Bow",
             description="Fiberglass Compound Bow.  Draw Weight 60-70 lbs.  Weight 3.8 lbs.  Right-hand only. Draw Length 25.5in to 31in.",
             category_name=category4.name)
            # price="$599.99",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Cross Bow",
             description="Whitetail Crossbow.  Includes quiver and two 20 inch arrows.",
             category_name=category4.name)
            # price="$349.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Carbon Arrows",
             description="Straightness: +/-.0025. Weight: +/- 1.0 grains. Package comes with 6 arrows. ",
             category_name=category4.name)
            # price="$49.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="Bow Case",
             description="Compact Bow Case. Patented PillarLock system. Weight: 10 lbs.",
             category_name=category4.name)
            # price="$39.99",
            # or category=category2)

session.add(Item4)
session.commit()



# Category for Tree Stands
category5 = Category(user_id=1,
                    name="Tree Stands")

session.add(category5)
session.commit()

print 'Category5 Name=' + category5.name

Item1 = Item(user_id=1,
             name="Summit Titan",
             description="Summit Titan Climbing Stand.  Platform: 20x30.75.  Max Weight: 350 lbs.",
             category_name=category5.name)
            # price="$349.99",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Summit The Viper Series",
             description="Summit Ultra Climbing Stand.  Seat: 18x12, Backrest: 12x20, Platform: 20x28.75.  Max Weigth: 300 lbs.",
             category_name=category5.name)
            # price="$249.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Ladder Stand",
             description="20' Ultra Steel Ladder Stand. Platform: 24x26, Height: 20' to shooting rail., Max Weight: 300lbs.",
             category_name=category5.name)
            # price="$229.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="Safety Harness",
             description="Gorilla Safety Harness. 30 in tether for 360 deg mobility.  Max Weight: 300 lbs.",
             category_name=category5.name)
            # price="$69.97",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Firearm Safes
category6 = Category(user_id=1,
                    name="Firearm Safes")

session.add(category6)
session.commit()

print 'Category6 Name=' + category6.name

Item1 = Item(user_id=1,
             name="19-Gun Safe",
             description="Fire Rating: 45 min at 1,400 deg F. Weight 276 lbs. 56x22x18. 12.8 cu ft.",
             category_name=category6.name)
            # price="$499.97",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="24-Gun Safe",
             description="Fire Rating: 45 min at 1,200 deg F. Weight 398 lbs. 60x28x20. 19 cu ft.  Includes a door panel organizer.",
             category_name=category6.name)
            # price="$699.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="25-Gun Safe",
             description="Fire Rating: 60 min at 1,400 deg F. Weight 515 lbs. 58x30x22. 23 cu ft.",
             category_name=category6.name)
            # price="$899.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="40-Gun Safe",
             description="Fire Rating: 45 min at 1,400 deg F. Weight 525 lbs. 58x36x27. 33 cu ft.",
             category_name=category6.name)
            # price="$1,199.99",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Knives
category7 = Category(user_id=1,
                    name="Knives")

session.add(category7)
session.commit()

print 'Category7 Name=' + category7.name

Item1 = Item(user_id=1,
             name="Uncle Henry Golden Spike",
             description="Bone handle.  Stanless steel blade.",
             category_name=category7.name)
            # price="$29.97",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Gerbr Field Dress",
             description="Gerber Moment Field Dress Cleaning Kit.  Includes gut hook, caping knife, and nylon sheath.",
             category_name=category7.name)
            # price="$29.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Extrem Survival Hatchet",
             description="Schrade Extreme Survival Hatchet.  Includes hard sheath and Ferro rod.",
             category_name=category7.name)
            # price="$29.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
            name="Pruner Saw Combo",
             description="Ridge Hunter Pruner Saw Combo.",
             category_name=category7.name)
            # price="$9.99",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Rifles
category8 = Category(user_id=1,
                    name="Rifles")

session.add(category8)
session.commit()

print 'Category8 Name=' + category8.name

Item1 = Item(user_id=1,
             name="Benjamin Airgun",
             description="Benjamin Guide Hawk Combo.  .22 cal, Alloy Pellets. 950 fps. Includs 3-9/32 scope.",
             category_name=category8.name)
            # price="$499.97",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Swarm Maxxim Combo",
             description="Swarm Maxxim Combo. 10-shot repeater.  3-9/40 scope with rings.",
             category_name=category8.name)
            # price="$179.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Savage",
             description="Savage 11/111 Trophy Hunter.  Assorted calibers.  Synthetic/Blued.",
             category_name=category8.name)
            # price="$499.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="Ruger American Rifle",
             description="Ruger American Rimfire Rifle.  .22 LR, 22 inch barrel, 10-rd, Black/Synthetic.",
             category_name=category8.name)
            # price="$299.99",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Ammunition
category9 = Category(user_id=1,
                    name="Ammunition")

session.add(category9)
session.commit()

print 'Category9 Name=' + category9.name

Item1 = Item(user_id=1,
             name="Federal Power-Shok",
             description=".308, 150 grain.  15 percent off while supplies last.",
             category_name=category9.name)
            # price="$19.97",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Federal Gold Medal",
             description="Federal Gold Medal, Centerfire Rifle Ammo, .308 168 grain.",
             category_name=category9.name)
            # price="$179.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Remington",
             description="Remington Long Range Express. 12 Guage.",
             category_name=category9.name)
            # price="$15.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="Remington 22",
             description="Remington 22 - Golden Bullet .22 LR Rimfire Ammo.",
             category_name=category9.name)
            # price="$299.99",
            # or category=category2)

session.add(Item4)
session.commit()


# Category for Scopes
category10 = Category(user_id=1,
                    name="Scopes")

session.add(category10)
session.commit()

print 'Category10 Name=' + category10.name

Item1 = Item(user_id=1,
             name="Riflescopes",
             description="Leupold - Made in USA.  2-7x33",
             category_name=category10.name)
            # price="$179.97",
            # or category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1,
             name="Thermal Viewer",
             description="Thermal Observation Viewer.  Find downed game in dense terrain - day or night.",
             category_name=category10.name)
            # price="$699.99",
            # or category=category2)

session.add(Item2)
session.commit()


Item3 = Item(user_id=1,
             name="Thermal Imager",
             description="Leupol Thermal Imager, Cameera and Flashlight.",
             category_name=category10.name)
            # price="$499.99",
            # or category=category2)

session.add(Item3)
session.commit()


Item4 = Item(user_id=1,
             name="Leupold Binoculars",
             description="Leupold Binoculars.  10x42 BX-1, McKenzie Binoculars.",
             category_name=category10.name)
            # price="$149.99",
            # or category=category2)

session.add(Item4)
session.commit()


print "Added Category items!"
