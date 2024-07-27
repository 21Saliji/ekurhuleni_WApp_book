const express = require('express');
const Booking = require('../models/Booking'); // Import the Booking model
const Venue = require('../models/Venue'); // Import the Venue model

const router = express.Router();

// Get all bookings
router.get('/', async (req, res) => {
  try {
    const bookings = await Booking.find().populate('venue');  
 // Populate venue details
    res.json(bookings);
  } catch (err) {
    console.error(err); // Log the error for debugging
    res.status(500).json({ message: 'Internal server error' }); // Generic error message for user
  }
});

// Get a specific booking
router.get('/:id', async (req, res) => {
  try {
    const booking = await Booking.findById(req.params.id).populate('venue');
    if (!booking) {
      return res.status(404).json({ message: 'Booking not found' });
    }
    res.json(booking);
  } catch (err) {
    console.error(err); // Log the error for debugging
    res.status(500).json({ message: 'Internal server error' }); // Generic error message for user
  }
});

// Create a new booking
router.post('/', async (req, res) => {
  const { venueId, ...bookingData } = req.body;

  try {
    const venue = await Venue.findById(venueId);
    if (!venue) {
      return res.status(404).json({ message: 'Venue not found' });
    }

    // Check venue availability (implement your logic here)

    const booking = new Booking({ ...bookingData, venue: venueId });
    const newBooking = await booking.save();
    res.status(201).json(newBooking);
  } catch (err) {
    console.error(err); // Log the error for debugging
    // Handle specific errors (e.g., validation errors) if needed
    res.status(400).json({ message: 'Bad request' }); // Generic message for user
  }
});

// Update a booking
router.put('/:id', async (req, res) => {
  try {
    const updatedBooking = await Booking.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!updatedBooking) {
      return res.status(404).json({ message: 'Booking not found'  
 });
    }
    res.json(updatedBooking);
  } catch (err)  
 {
    console.error(err); // Log the error for debugging
    res.status(400).json({ message: 'Bad request' }); // Generic message for user
  }
});

// Delete a booking
router.delete('/:id', async (req, res) => {
  try {
    const deletedBooking = await Booking.findByIdAndDelete(req.params.id);
    if (!deletedBooking) {
      return res.status(404).json({ message: 'Booking not found' });
    }
    res.json({  
 message: 'Booking deleted' });
  } catch (err) {
    console.error(err); // Log the error for debugging
    res.status(500).json({ message: 'Internal server error' }); // Generic message for user
  }
});

module.exports = router;

// ... rest of your booking controller code

// Create a new booking
router.post('/', async (req, res) => {
    const { venueId, startDate, endDate, startTime, endTime, numberOfGuests, ...bookingData } = req.body;
  
    try {
      const venue = await Venue.findById(venueId);
      if (!venue) {
        return res.status(404).json({ message: 'Venue not found' });
      }
  
      // Check venue capacity
      const existingBookings = await Booking.find({
        venue: venueId,
        startDate: { $lte: endDate },
        endDate: { $gte: startDate }
      });
  
      let totalGuests = 0;
      existingBookings.forEach(booking => {
        totalGuests += booking.numberOfGuests;
      });
  
      if (totalGuests + numberOfGuests > venue.capacity) {
        return res.status(400).json({ message: 'Venue capacity exceeded' });
      }
  
      // Check for overlapping bookings based on start and end times
      const overlappingBookings = existingBookings.filter(booking => {
        return !(endTime <= booking.startTime || startTime >= booking.endTime);
      });
  
      if (overlappingBookings.length > 0) {
        return res.status(400).json({ message: 'Venue is not available for the specified time' });
      }
  
      // Create the booking
      const booking = new Booking({ ...bookingData, venue: venueId, startDate, endDate, startTime, endTime, numberOfGuests });
      const newBooking = await booking.save();
      res.status(201).json(newBooking);
    } catch (err) {
      res.status(400).json({ message: err.message });
    }
  });
  