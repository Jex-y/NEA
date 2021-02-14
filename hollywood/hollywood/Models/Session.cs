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
    }
}
