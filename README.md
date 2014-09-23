python-pistage
==============

**This software is not associated with Ocean Optics. Use it at your own risk.**

## PI nano Pizeo Stage Controller python module ##

This python module provides access to some basic functionality for PI nano Piezo Stage 
Controllers. PI also distributes a bindings for their c++ library, but this python module uses 
the simple Serial Interface most controllers provide, which is more straightforward to use (IMHO).

**If you are not 100% sure what you are doing, stick with
the software supplied by PI.**

## Status ##

At the moment work is only done for the E-545 Controller, because that's the System that I use. 

## Quickstart ##

After installing test if it's working by:

```
import PIStage
stage = PIStage.E545()
print stage.pos()
```

## Contributing ##

Feel free to contribute :)
