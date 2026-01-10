    // Configuration - enter start date: "2026-01-09T00:00:00"
    const startDate = new Date('2026-01-09T04:00:00').getTime();
    
    // Set freezeTime to null to keep it running. 
    // To freeze it, enter the date/time (e.g., '2026-01-10T02:00:00') empty: 'null'
    let freezeTime = '2026-01-10T10:50:01'; 

    function updateTimer() {
      const now = new Date().getTime();
      
      // Determine which end-point to use: the current time or the freeze time
      const effectiveEnd = (freezeTime && now >= new Date(freezeTime).getTime()) 
                           ? new Date(freezeTime).getTime() 
                           : now;

      const difference = effectiveEnd - startDate;

      if (difference < 0) {
        document.getElementById("display").innerText = "00:00:00";
        return;
      }

      const hours = Math.floor(difference / (1000 * 60 * 60));
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((difference % (1000 * 60)) / 1000);

      document.getElementById("display").innerText = 
        `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

      // If we have reached or passed the freeze time, stop the interval
      if (freezeTime && now >= new Date(freezeTime).getTime()) {
        clearInterval(timerInterval);
        console.log("Clock Frozen at: " + freezeTime);
      }
    }

    const timerInterval = setInterval(updateTimer, 1000);
    updateTimer();

    /** * HELPER FUNCTION: 
     * You can call freezeClock() from the browser console to stop it manually.
     */
    function freezeClock() {
        freezeTime = new Date().toISOString();
        updateTimer();
    }