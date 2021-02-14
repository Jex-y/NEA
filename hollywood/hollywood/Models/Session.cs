using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    public class Session
    {
        [JsonProperty("sessId")]
        public Guid SessId { get; set; }

        //[JsonProperty("startTime")]
        //public DateTime StartTime { get; set; }

        //[JsonProperty("endTime")]
        //public DateTime EndTime { get; set; }
        // Dont need to be stored by client, sever just needs open and close methods.
    }
}
