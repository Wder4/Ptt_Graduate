using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using WebSocketSharp;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Diagnostics;
using System.Windows.Threading;
using System.Threading;
using System.Collections.ObjectModel;

namespace PTT_UI
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            WS_Init();
        }

        public class Ptt_Unit_Pack
        {
            public string date { get; set; }
            public string title { get; set; }
            public string url { get; set; }
        }

        private void sch_btn_Click(object sender, RoutedEventArgs e)
        {
            Send_Order("Ptt_List", "");
        }
        
        public void Show_Ptt_List(DataGrid Main_Grid, JArray Data_List)
        {
            var Data_Grid_List = new ObservableCollection<Ptt_Unit_Pack>();           
            foreach (var item in Data_List)
            {
                var new_unit_item = new Ptt_Unit_Pack();
                new_unit_item.date = (string)item["date"];
                new_unit_item.title = (string)item["title"];
                new_unit_item.url = (string)item["url"];
                Data_Grid_List.Add(new_unit_item);
            }

            Dispatcher.Invoke(
                DispatcherPriority.Normal,
                new Action<DataGrid, ObservableCollection<Ptt_Unit_Pack>>
                (Change_DataGrid_Source), Main_Grid, Data_Grid_List
                );

        }
        public void Change_DataGrid_Source(DataGrid DG, ObservableCollection<Ptt_Unit_Pack> source)
        {
            DG.ItemsSource = source;
        }

        // WS 連線設定  WebSocket Client
        private WebSocket WS;
        const string host = "ws://127.0.0.1:6688";
        public void WS_Init()
        {
            WS = new WebSocket(host);
            WS.OnMessage += (ss, ee) =>   // receive a message 
                Msg_Decode(ee.Data);
            WS.OnOpen += (ss, ee) =>      // connection has been established
                Onopen_fn(ss, ee);
            WS.OnError += (sender, e) =>  // gets an error
                On_Error_fn(sender, e);
            WS.OnClose += (sender, e) =>  // close the connection
                On_Close_fn(sender, e);
            WS.Connect();
        }


        private void Msg_Decode(string json)
        {
            //console.writeline("ws_接到訊息: ");
            //console.writeline(json);
            try
            {
                dynamic data = JValue.Parse(json);
                string order = data["order"];
                var detail = data["detail"];
                switch (order)
                {
                    case "Ptt_List":
                        //string logtxt = (string)detail;
                        Show_Ptt_List(PTT_List, detail);
                        break;
                    default:
                        Console.WriteLine(json);
                        break;
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                Console.WriteLine(json);
                Console.WriteLine("error_WS_Msg_not a JSON");
            }
        }

        private void Onopen_fn(object ss, EventArgs e)
        {
            Dispatcher.Invoke(
                       DispatcherPriority.Normal,
                       new Action<Label, string>(Change_Label_Text),
                       WS_Con_Stat, "Connect"
                       );
        }

        private void On_Error_fn(object ss, WebSocketSharp.ErrorEventArgs e)
        {
            Debug.WriteLine("WS_Error");
            Debug.WriteLine(e);
        }

        private void On_Close_fn(object ss, CloseEventArgs e){
            Debug.WriteLine("WS_Close");
            Debug.WriteLine(WS.ReadyState);
            Dispatcher.Invoke(
                         DispatcherPriority.Normal,
                         new Action<Label, string>(Change_Label_Text),
                         WS_Con_Stat, "已斷線" 
                         );
            //自動重連
            while (WS.ReadyState.ToString() == "Closed"){
                Thread.Sleep(1000);
                WS.Connect();
            }
        }
   
        private void Change_Label_Text(Label Lab, string txt)
        {
            Lab.Content = txt;
        }

        private void Send_Order(string order, dynamic detail)
        {
            JObject data = new JObject();
            data["order"] = order;
            data["detail"] = detail;
            string json = data.ToString(Formatting.None);
            WS.Send(json);
        }


    }


}
