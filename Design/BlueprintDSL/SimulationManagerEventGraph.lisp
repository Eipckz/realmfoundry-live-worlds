(event EventBeginPlay
  (Variables|Default|SetDay 1)
  (Variables|Default|SetSubscribers 250)
  (Variables|Default|SetActivePlayers 186)
  (Variables|Default|SetProgressStep 0)
  (Variables|Default|SetServersOnline true)
  (Variables|Default|SetObjectiveComplete false)
  (Development|PrintString "LIVE MMO SIMULATION ONLINE // 250 INDIVIDUAL SUBSCRIBERS PLANNING ACTIVITIES" true true "(R=0.120000,G=0.900000,B=1.000000,A=1.000000)" 10.0)
  (Development|PrintString "BUILD SIX SERVICES FROM THE TOP-DOWN STRATEGY CAMERA, THEN PRESS R TO SHIP THE MAJOR UPDATE" true true "(R=0.250000,G=1.000000,B=0.520000,A=1.000000)" 10.0))

(event Custom|EventBeginPlay)

(event Custom|SimTick)

(event Collision|EventActorBeginOverlap (OtherActor))

(event EventTick (DeltaSeconds))
