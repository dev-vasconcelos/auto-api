using System;
using System.Collections.Generic;

namespace Rfid.Response
{
    public class ResponseEntity<T>
    {
        public IEnumerable<string> errors { get; set; }
        public T data { get; set; }

        public ResponseEntity(T data, string messageError)
        {
            var list = new List<string>();
            list.Add(messageError);
            errors = list;
            this.data = data;

        }
        public ResponseEntity(T data, IEnumerable<string> errors)
        {
            this.data = data;
            this.errors = errors;
        }
        public ResponseEntity(T data, Exception ex)
        {
            var list = new List<string>();
            list.Add(ex.Message);
            errors = list;
            this.data = data;
        }
        public ResponseEntity(T data)
        {
            this.data = data;
        }

        public ResponseEntity()
        {
        }

    }
}
