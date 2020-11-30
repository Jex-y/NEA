using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Newtonsoft.Json;
using Xamarin.Forms;

namespace hollywood.Models
{
    public class MenuHandle
    {
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("url_name")]
        public string URLName { get; set; }
        [JsonProperty("description")]
        public string Description { get; set; }
        [JsonProperty("image")]
        public Uri ImageURI { get; set; }

        public ICommand Tapped => new Command(async () => await tapped());

        async Task tapped() {
            Debug.WriteLine("Was tapped");
        } 
    }
}
