#!/bin/bash
# ------------------------------------------------------------------------------
# Copyright 2002-2011, GridWay Project Leads (GridWay.org)          
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

# Common initialization
if [ -z "${GW_LOCATION}" ]; then
    export GW_LOCATION=`dirname $0`
fi

. $GW_LOCATION/bin/gw_mad_common.sh

setup_globus
cd_var
mad_debug
check_proxy

if [ -z "${GLOBUS_TCP_PORT_RANGE}" ]; then
    exec nice -n $PRIORITY java -DGLOBUS_LOCATION=$GLOBUS_LOCATION -Djava.endorsed.dirs=$GLOBUS_LOCATION/endorsed GWRftProcessor
else
    exec nice -n $PRIORITY java -DGLOBUS_LOCATION=$GLOBUS_LOCATION -Djava.endorsed.dirs=$GLOBUS_LOCATION/endorsed -DGLOBUS_TCP_PORT_RANGE=$GLOBUS_TCP_PORT_RANGE GWRftProcessor
fi
